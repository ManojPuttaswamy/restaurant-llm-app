import json
import streamlit as st
import pandas as pd

from src.config import get_openai_key
from src.llm import build_llm
from src.service import generate_full_concept, generate_brand_kit, generate_menu
from src.utils import ensure_menu_rows

st.set_page_config(page_title="Restaurant Concept Studio", page_icon="🍽️", layout="wide")

# ---- Minimal modern styling
st.markdown(
    """
    <style>
      .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
      div[data-testid="stMetric"] {border-radius: 16px; padding: 10px 12px;}
      .stTabs [data-baseweb="tab-list"] button {border-radius: 12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Restaurant Concept Studio")
st.caption("Brand Kit with Structured Menu (with pricing)")

# ---- Load key
try:
    key = get_openai_key()
except Exception as e:
    st.error(str(e))
    st.stop()

# ---- Sidebar controls (modern app feel)
with st.sidebar:
    st.header("Controls")
    cuisine = st.text_input("Cuisine", value=st.session_state.get("cuisine", "Mexican"))
    theme = st.selectbox(
        "Theme",
        ["Fine Dining", "Street Food", "Family Friendly", "Modern Fusion", "Coastal", "Chef’s Tasting"],
        index=0,
    )
    price_range = st.selectbox("Price Range", ["20", "40", "50", "100"], index=1)

    st.subheader("Dietary filters")
    vegan = st.checkbox("Vegan")
    vegetarian = st.checkbox("Vegetarian")
    gluten_free = st.checkbox("Gluten-free")
    nut_free = st.checkbox("Nut-free")
    halal = st.checkbox("Halal")

    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.6, 0.1)

    st.divider()
    generate_all = st.button("Generate full concept", type="primary", use_container_width=True)
    regen_brand = st.button("Regenerate brand kit", use_container_width=True)
    regen_menu = st.button("Regenerate menu", use_container_width=True)

def dietary_notes() -> str:
    tags = []
    if vegan: tags.append("vegan")
    if vegetarian: tags.append("vegetarian")
    if gluten_free: tags.append("gluten-free")
    if nut_free: tags.append("nut-free")
    if halal: tags.append("halal")
    return ", ".join(tags)

# ---- LLM
llm = build_llm(key, temperature=temperature)

# ---- Session state for persistence + regen
if "brand" not in st.session_state:
    st.session_state.brand = None
if "menu" not in st.session_state:
    st.session_state.menu = None

# ---- Actions
if generate_all:
    st.session_state.cuisine = cuisine
    with st.spinner("Generating brand kit + menu..."):
        try:
            concept = generate_full_concept(llm, cuisine, theme, price_range, dietary_notes())
            st.session_state.brand = concept["brand"]
            st.session_state.menu = concept["menu"]
        except Exception as e:
            st.error(f"Generation failed: {e}")

if regen_brand:
    with st.spinner("Regenerating brand kit..."):
        try:
            st.session_state.brand = generate_brand_kit(llm, cuisine, theme, price_range)
        except Exception as e:
            st.error(f"Brand regeneration failed: {e}")

if regen_menu:
    with st.spinner("Regenerating menu..."):
        try:
            name = (st.session_state.brand or {}).get("restaurant_name") or "Restaurant"
            st.session_state.menu = generate_menu(llm, name, cuisine, theme, price_range, dietary_notes())
        except Exception as e:
            st.error(f"Menu regeneration failed: {e}")

brand = st.session_state.brand
menu_obj = st.session_state.menu

# ---- Top summary cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cuisine", cuisine)
c2.metric("Theme", theme)
c3.metric("Price", price_range)
c4.metric("Dietary", dietary_notes() or "None")

st.divider()

# ---- Main content
tab1, tab2 = st.tabs(["Brand Kit", "Menu"])

with tab1:
    if not brand:
        st.info("Use the sidebar → **Generate full concept** to create your Brand Kit.")
    else:
        name = brand.get("restaurant_name", "—")
        tagline = brand.get("tagline", "—")
        story = brand.get("brand_story", "—")

        st.subheader(name)
        st.write(f"**Tagline:** {tagline}")
        st.write(story)

        a = brand.get("ambience", {}) if isinstance(brand.get("ambience"), dict) else {}
        vibe = a.get("vibe_keywords", [])
        music = a.get("music", "—")
        interior = a.get("interior", "—")

        st.markdown("#### Ambience")
        colA, colB = st.columns([1, 1])
        with colA:
            st.write("**Vibe keywords**")
            if isinstance(vibe, list) and vibe:
                st.write(" • " + "\n • ".join([str(x) for x in vibe]))
            else:
                st.write("—")
            st.write("**Music**")
            st.write(music)
        with colB:
            st.write("**Interior**")
            st.write(interior)

        t = brand.get("target_customer", {}) if isinstance(brand.get("target_customer"), dict) else {}
        st.markdown("#### Target Customer")
        st.write(f"**Persona:** {t.get('persona','—')}")
        st.write(f"**Why they come:** {t.get('why_they_come','—')}")

        st.download_button(
            "Download Brand Kit JSON",
            data=json.dumps(brand, indent=2),
            file_name="brand_kit.json",
            mime="application/json",
            use_container_width=False,
        )

with tab2:
    if not menu_obj:
        st.info("Generate the concept first to see a structured menu table.")
    else:
        rows = ensure_menu_rows(menu_obj.get("menu"))
        if not rows:
            st.warning("Menu JSON came back empty. Try regenerating the menu.")
        else:
            df = pd.DataFrame(rows)

            # Make sure columns exist
            for col in ["category", "item", "description", "price_usd"]:
                if col not in df.columns:
                    df[col] = ""

            # Sort to look nice
            order = {"Starter": 0, "Main": 1, "Dessert": 2, "Drink": 3}
            df["__order"] = df["category"].map(order).fillna(99).astype(int)
            df = df.sort_values(["__order", "price_usd"], ascending=[True, True]).drop(columns=["__order"])

            st.subheader("Menu")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "category": st.column_config.TextColumn("Category", width="small"),
                    "item": st.column_config.TextColumn("Item", width="medium"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "price_usd": st.column_config.NumberColumn("Price (USD)", format="$%.2f", width="small"),
                },
            )

            st.download_button(
                "Download Menu JSON",
                data=json.dumps(menu_obj, indent=2),
                file_name="menu.json",
                mime="application/json",
            )

            # Optional combined export if brand exists
            if brand:
                combined = {"brand": brand, "menu": menu_obj}
                st.download_button(
                    "Download Full Concept JSON",
                    data=json.dumps(combined, indent=2),
                    file_name="restaurant_concept.json",
                    mime="application/json",
                )