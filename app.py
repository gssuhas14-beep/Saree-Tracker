import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# App page configuration optimized for iOS mobile view
st.set_page_config(page_title="Saree Loom Tracker", page_icon="🧵", layout="centered")
st.title("🧵 Saree Loom Tracker")

# Local Storage Simulation: Keeps data safe in your phone's active browser session
if 'ledger' not in st.session_state:
    st.session_state.ledger = pd.DataFrame(columns=["Date", "Loom", "Weaver ID", "Design No", "Colour", "Pcs Woven"])

# --- TAB VIEW LAYOUT ---
tab1, tab2 = st.tabs(["📝 Log Daily Production", "📊 Weekly Weaver Reports"])

with tab1:
    st.header("Record Daily Output")
    
    # Date Input Selection
    date_input = st.date_input("Production Date", datetime.now())
    
    # EXACT SEQUENCE: 1 to 16, then S1 to S8
    loom_options = [str(i) for i in range(1, 17)] + [f"S{i}" for i in range(1, 9)]
    selected_loom = st.selectbox("Select Loom Number", loom_options)
    
    # Weaver ID input box
    weaver_id = st.text_input("Weaver ID (e.g., Weaver 1, Weaver 2)", placeholder="Type Weaver Name/ID here")
    
    # Design and Custom Colour text fields
    design_no = st.text_input("Design Number / Chapa No.", placeholder="e.g., 4055")
    saree_colour = st.text_input("Saree Colour (Type Any Color)", placeholder="e.g., Royal Blue, Rani Pink")
    
    # Quantity Counter
    pcs_woven = st.number_input("Total Pieces Woven Today", min_value=1, step=1, value=1)
    
    # Save Transaction Button
    if st.button("Save Daily Entry", use_container_width=True):
        if design_no and saree_colour and weaver_id:
            new_entry = {
                "Date": date_input.strftime("%Y-%m-%d"),
                "Loom": selected_loom,
                "Weaver ID": weaver_id.strip().title(),
                "Design No": design_no.strip(),
                "Colour": saree_colour.strip().title(),
                "Pcs Woven": int(pcs_woven)
            }
            # Append entry to the database
            st.session_state.ledger = pd.concat([st.session_state.ledger, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"Successfully Saved {pcs_woven} Pcs on Loom {selected_loom}!")
        else:
            st.error("Please fill in Weaver ID, Design Number, and Saree Colour to save.")

# --- TAB 2: REPORTS & WEEKLY CALCULATOR ---
with tab2:
    st.header("Production History & Analysis")
    
    if st.session_state.ledger.empty:
        st.info("No records logged yet. Go to the entry tab to log production.")
    else:
        df = st.session_state.ledger.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Pcs Woven"] = df["Pcs Woven"].astype(int)
        
        # 7-Day Weaver Production Calculator
        st.subheader("🧮 7-Day Weaver Production Summary")
        one_week_ago = datetime.now() - timedelta(days=7)
        weekly_df = df[df["Date"] >= one_week_ago]
        
        if not weekly_df.empty:
            weaver_totals = weekly_df.groupby("Weaver ID")["Pcs Woven"].sum().reset_index()
            weaver_totals.columns = ["Weaver Identifier", "Total Sarees Done (Last 7 Days)"]
            st.dataframe(weaver_totals, use_container_width=True, hide_index=True)
        else:
            st.write("No production entries found within the past 7 days.")
            
        # Entire Ledger Table View
        st.subheader("📋 Complete Ledger Book")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download ledger straight to iPhone storage
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Ledger as Excel/CSV File",
            data=csv,
            file_name=f"saree_production_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
