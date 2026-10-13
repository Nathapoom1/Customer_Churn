from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


MODEL_PATH = Path(__file__).parent / "model" / "churn_pipeline.joblib"

st.set_page_config(
    page_title="ประเมินความเสี่ยงลูกค้า",
    page_icon="📊",
    layout="centered",
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


st.title("ประเมินความเสี่ยงการยกเลิก")
st.caption("Customer churn prediction · กรอกข้อมูลการใช้งานเพื่อประเมินแนวโน้ม churn")

if not MODEL_PATH.exists():
    st.error("ยังไม่พบไฟล์โมเดล กรุณารันส่วน Export model ใน Customer_Churn.ipynb ก่อน")
    st.stop()

model = load_model()

with st.form("customer_input"):
    st.subheader("ข้อมูลลูกค้า")
    left, right = st.columns(2)

    with left:
        months_member = st.number_input(
            "ระยะเวลาสมาชิก (เดือน)", min_value=0, value=12, step=1
        )
        monthly_fee = st.number_input(
            "ค่าบริการต่อเดือน", min_value=0.0, value=500.0, step=50.0, format="%.2f"
        )
        usage_hours_month = st.number_input(
            "ชั่วโมงใช้งานต่อเดือน", min_value=0.0, value=30.0, step=1.0, format="%.1f"
        )

    with right:
        support_calls = st.number_input(
            "จำนวนครั้งที่ติดต่อ Support", min_value=0, value=1, step=1
        )
        late_payments = st.number_input(
            "จำนวนครั้งที่ชำระล่าช้า", min_value=0, value=0, step=1
        )
        contract_type = st.selectbox(
            "ประเภทสัญญา", ["Monthly", "Annual", "Two-Year", "Unknown"]
        )

    submitted = st.form_submit_button(
        "ประเมินความเสี่ยง", type="primary", icon=":material/analytics:"
    )

if submitted:
    row = pd.DataFrame([{
        "months_member": months_member,
        "monthly_fee": monthly_fee,
        "support_calls": support_calls,
        "usage_hours_month": usage_hours_month,
        "late_payments": late_payments,
        "contract_type": contract_type,
    }])

    prediction = int(model.predict(row)[0])
    probability = (
        float(model.predict_proba(row)[0, 1])
        if hasattr(model, "predict_proba")
        else None
    )

    with st.container(border=True):
        st.subheader("ผลการประเมิน")
        result_col, probability_col = st.columns(2)
        with result_col:
            st.metric(
                "แนวโน้มจากโมเดล",
                "มีแนวโน้มยกเลิก" if prediction == 1 else "ไม่พบแนวโน้มยกเลิก",
            )
        if probability is not None:
            with probability_col:
                st.metric("ความน่าจะเป็น churn", f"{probability:.1%}")
            st.progress(probability, text="ระดับความน่าจะเป็น churn")

        st.caption("ผลนี้เป็นการประเมินจากโมเดล ไม่ใช่การยืนยันว่าลูกค้าจะยกเลิกแน่นอน")
