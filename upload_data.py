import pandas as pd
from sqlalchemy import create_engine

# 1. สร้าง Connection String
# รูปแบบ: 'postgresql://username:password@localhost:5432/database_name'
DB_URL = 'postgresql://datascientist:mypassword@localhost:5432/bigdata_db'

# 2. สร้าง Engine เพื่อเชื่อมต่อ
engine = create_engine(DB_URL)

def upload_to_db(file_path, table_name):
    try:
        # 3. อ่านข้อมูล (สมมติว่าเป็นไฟล์ Big Data .csv)
        # ใช้ chunksize เพื่อไม่ให้แรมเต็มเวลาเจอข้อมูลระดับล้านแถว
        print("กำลังอ่านข้อมูล...")
        df_iter = pd.read_csv(file_path, chunksize=10000)

        for i, chunk in enumerate(df_iter):
            # 4. ส่งข้อมูลเข้า Postgres
            # if_exists='append' คือการเพิ่มข้อมูลต่อท้ายไปเรื่อยๆ
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"ส่งข้อมูล Chunk ที่ {i+1} สำเร็จ")

        print("ข้อมูลทั้งหมดถูกเก็บใน PostgreSQL แล้ว")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
