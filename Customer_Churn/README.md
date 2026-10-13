# Customer Churn Classification

โครงงานจำแนกการยกเลิกบริการ (`churn`) จากไฟล์ `C03_customer_churn_classification.xlsx`

## เริ่มต้น

1. ติดตั้ง Python 3.10 ขึ้นไป แล้วเปิด Terminal ที่โฟลเดอร์นี้
2. ติดตั้งแพ็กเกจด้วย `pip install -r requirements.txt`
3. เปิดและรัน `Customer_Churn.ipynb` จากบนลงล่าง
4. ตรวจผลเทียบโมเดลและเลือกโมเดลจาก **validation set** ก่อนวัดผลชุดทดสอบ

โน้ตบุ๊กตรวจ schema/คุณภาพข้อมูล, ทำ EDA อย่างน้อย 3 กราฟ, เตรียมข้อมูลด้วย scikit-learn Pipeline และเปรียบเทียบ Logistic Regression, Random Forest และ K-Nearest Neighbors (KNN) ด้วย Accuracy, Precision, Recall, F1, Confusion Matrix และ ROC-AUC โดยเลือกโมเดลจาก validation ก่อนฝึกซ้ำด้วย train และ validation แล้วประเมินบน test

## Deploy แบบที่ 1: Streamlit

หลังรันโน้ตบุ๊กจนถึงส่วน export โมเดล:

```bash
streamlit run app.py
```

### เผยแพร่เว็บออนไลน์ผ่าน Streamlit Community Cloud

Community Cloud ดึงแอปจาก GitHub โดยไฟล์ที่จำเป็นต้องอยู่ใน repository มีดังนี้:

```text
app.py
requirements.txt
.streamlit/config.toml
model/churn_pipeline.joblib
```

ไม่จำเป็นต้องอัปโหลดไฟล์ Excel, โน้ตบุ๊ก หรือ `api.py` เพื่อรันหน้าเว็บ Streamlit หากไม่ต้องการเผยแพร่ข้อมูลต้นทาง

1. สร้าง GitHub repository แล้วอัปโหลดไฟล์ข้างต้นโดยคงโครงสร้างโฟลเดอร์ไว้
2. เข้า [Streamlit Community Cloud](https://share.streamlit.io/) แล้วเชื่อมบัญชี GitHub
3. เลือก **Create app** ระบุ repository, branch และ app file path เป็น `app.py`
4. ใน **Advanced settings** เลือก Python 3.14 ให้ตรงกับ environment ที่สร้างโมเดล
5. กด **Deploy** แล้วรอ build เสร็จ จากนั้นส่ง URL ของแอปให้อาจารย์

เวอร์ชันของ NumPy, pandas, scikit-learn, joblib และ Streamlit ถูก pin ไว้ใน `requirements.txt` เพื่อให้สภาพแวดล้อมออนไลน์ตรงกับที่สร้างและทดสอบโมเดล

## Deploy แบบที่ 2: FastAPI

```bash
uvicorn api:app --reload
```

เปิด `/docs` เพื่อทดลองส่งข้อมูลให้ API ทั้งสองแบบต้องมี `model/churn_pipeline.joblib` ซึ่งโน้ตบุ๊กสร้างให้ในขั้นตอน export

## ข้อควรระวังในการตีความ

- `customer_id` เป็น identifier จึงไม่ใช้เป็น feature
- แก้ตัวพิมพ์ใน `contract_type` และรวมค่าว่างเป็น `Unknown`; impute ตัวเลขด้วย median ภายใน pipeline
- ลบแถวซ้ำ แต่ตรวจค่าผิดปกติและคงไว้ก่อน เพราะยังไม่มีหลักฐานว่าค่านั้นเป็นข้อผิดพลาด
- ชุดข้อมูลเป็นงานฝึกหัด ไม่ควรใช้ตัดสินใจต่อลูกค้าจริงโดยไม่มีการตรวจสอบผลกระทบและติดตามคุณภาพโมเดล
