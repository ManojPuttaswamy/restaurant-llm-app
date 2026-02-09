# Restaurant Concept Studio (LangChain + Streamlit)

Restaurant Concept Studio is a modern Streamlit app that generates a complete restaurant concept from a cuisine idea — including a **Brand Kit** (name, tagline, story, ambience, persona) and a **structured menu with pricing**.  
Built with a **modular architecture** using LangChain + OpenAI, designed to be beginner-friendly

---

## Features

### Brand Kit (JSON)
Generates:
- Restaurant name
- Tagline
- Short brand story
- Ambience (vibe keywords, music, interior design)
- Target customer persona + “why they come”

### Menu Generator (JSON → Table)
Generates a **structured menu**:
- Categories: Starter / Main / Dessert / Drink  
- Item name, description, and **realistic USD pricing**
- Rendered as a clean Streamlit table
- Exportable JSON downloads

### Modern UI
- Sidebar controls: cuisine, theme, price range, dietary filters, creativity slider
- Tabs: Brand Kit + Menu Table
- Regenerate Brand / Regenerate Menu
- Download Brand Kit JSON / Menu JSON / Full Concept JSON

---

## Tech Stack

- Python
- Streamlit
- LangChain (OpenAI integration)
- OpenAI API
- dotenv

---

