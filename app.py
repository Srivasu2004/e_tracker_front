import streamlit as st
import requests
import pandas as pd
server_loc=st.secrets["server_url"]
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)
st.title("💰EXPENSIVE TRACKER")
opt=st.sidebar.selectbox("choose operations:--",["add_expression","view_expression","update_expression","delete_expression","search_expression","sort_expression" ,"filter_expression",
        "analyze_spending"])
if opt == "add_expression":
    st.header("➕ ADDING EXPENSES")
    with st.form("add_expression"):
        name = st.text_input("👤Name")
        amount=st.number_input("💵amount")
        category=st.selectbox("category",[ "🍔 Food",
                "✈️ Travel",
                "🏠 Rent",
                "👕costume"])
        date=st.date_input("📅 Enter the date")
        btn=st.form_submit_button("add_expression")
        if btn:
            
            
            new_data = {
                "n":name,
                "a":amount,
                "c":category,
                "d":str(date)
            }
            response=requests.post(f"{server_loc}/add_exp",json= new_data)
            data=response.json()
            st.write(data)
            if response.status_code == 200:
                st.success("✅THE AMOUNT WAS SUFFICENT")
            else:
                st.error("❌ THE AMOUNT WAS NOT SUFFICENT")
elif opt== "view_expression":
    st.header("📋 VEIW EXPENSES")
    btn=st.button("view data")
    if btn:
        response = requests.get(f"{server_loc}/view_exp")
        data = response.json()  
        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("No employee data found")
elif opt == "update_expression":

    st.header("✏️ UPDATED EXPENSES")

    with st.form("update_expression_form"):
        id = st.number_input("Enter Employee ID", min_value=1)

        name = st.text_input("👤 Name")

        amount = st.number_input(
            "💵 Amount",
            min_value=0.0,
            format="%.2f"
        )

        category = st.selectbox(
            "📂 Category",
            [
                "🍔 Food",
                "✈️ Travel",
                "🏠 Rent",
                "👕 Costume"
            ]
        )

        date = st.date_input("📅 Select Date")

        update_btn = st.form_submit_button("Update Expense")

        if update_btn:

            updated_data = {
                "n": name,
                "a": amount,
                "c": category,
                "d": str(date)
            }

            try:
                response = requests.put(
                    f"{server_loc}/upd_exp/{id}",
                    json=updated_data
                )

                data = response.json()

                if response.status_code == 200:
                    st.success("✅ Expense Updated Successfully")
                    st.write(data)
                else:
                    st.error("❌ Expense Not Found")
                    st.write(data)

            except requests.exceptions.ConnectionError:
                st.error("❌ Unable to connect to FastAPI server")
elif opt  == "delete_expression":
    st.header("DELETE EXPENSES")
    id=st.number_input("🆔enter id", min_value=1)
    if st.button("🗑️ Delete Employee"):
        response = requests.delete(
            f"{server_loc}/delete_exp/{id}"
        )

        data = response.json()

        st.write(data)

        if response.status_code == 200:
            st.success("✅ Employee deleted successfully")
        else:
            st.error("❌Delete failed")
if opt=="search_expression":
    st.header("SEARCH DETAILS")
    id=st.number_input("enter the number")
    if st.button("search expression"):
        response=requests.get(f"{server_loc}/srh_exp/{id}")
        data =response.json()
        st.write(data)
        
        if response.status_code == 200:
                if "message" not in data:

                    st.success("✅ Expense Found")

                    df = pd.DataFrame([data])

                    st.dataframe(df)

                else:

                    st.warning("⚠️ Expense ID Not Found")

                    st.write(data)

        else:

                st.error("❌ Search Failed")
elif opt== "sort_expression":
    st.header("SORTING EXPRESSIONS")
    sort_by = st.selectbox(
        "🔽 Select Sort Column",
        [
            "id",
            "name",
            "amount",
            "category",
            "expense_date"
        ]
    )

    order = st.selectbox(
        "↕️ Select Order",
        [
            "ASC",
            "DESC"
        ]
    )

    if st.button("📊 Sort Expenses"):

        try:

            response = requests.get(
                f"{server_loc}/sort_exp/{sort_by}/{order}"
            )

            data = response.json()

            st.write(data)

            if response.status_code == 200:

                if len(data) > 0:

                    st.success("✅ Expenses Sorted Successfully")

                    df = pd.DataFrame(data)

                    st.dataframe(df)

                else:

                    st.warning("⚠️ No Data Found")

            else:

                st.error("❌ Sorting Failed")

        except requests.exceptions.ConnectionError:

            st.error("🚫 Unable to connect to FastAPI Server")
elif opt == "filter_expression":

    st.header("🔍 FILTER EXPENSES")

    category = st.selectbox(
        "📂 Select Category",
        [
            "🍔 Food",
            "✈️ Travel",
            "🏠 Rent",
            "👕 Costume"
        ]
    )

    if st.button("Filter Expenses"):

        try:

            response = requests.get(
                f"{server_loc}/filter_exp/{category}"
            )

            data = response.json()

            st.write(data)

            if response.status_code == 200:

                if len(data) > 0:

                    st.success("✅ Filter Applied Successfully")

                    df = pd.DataFrame(data)

                    st.dataframe(df)

                else:

                    st.warning("⚠️ No Expenses Found")

            else:

                st.error("❌ Filter Failed")

        except requests.exceptions.ConnectionError:

            st.error("🚫 Unable to connect to FastAPI Server")
elif opt == "analyze_spending":

    st.header("📊 ANALYZE SPENDING")

    if st.button("Analyze Expenses"):

        try:

            response = requests.get(
                f"{server_loc}/analyze_exp"
            )

            data = response.json()

            st.write(data)

            if response.status_code == 200:

                st.success("✅ Expense Analysis Completed")

                # Convert dictionary to dataframe
                analysis_df = pd.DataFrame(
                    list(data.items()),
                    columns=["Category", "Total Amount"]
                )

                st.dataframe(analysis_df)

                st.bar_chart(
                    analysis_df.set_index("Category")
                )

            else:

                st.error("❌ Analysis Failed")

        except requests.exceptions.ConnectionError:

            st.error("🚫 Unable to connect to FastAPI Server")
