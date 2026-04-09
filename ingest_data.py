import pandas as pd
from sqlalchemy import create_engine
import time

# 1. เชื่อมต่อ PostgreSQL
DB_URL = 'postgresql://datascientist:mypassword@127.0.0.1:5433/bigdata_db'
engine = create_engine(DB_URL)

def clean_and_ingest(file_path):
    t_start = time.time()
    
    # 2. อ่านข้อมูล Parquet
    print(f"--- กำลังอ่านไฟล์: {file_path} ---")
    df = pd.read_parquet(file_path)
    
    # 3. Data Cleaning เบื้องต้น (หัวใจของ Data Scientist)
    print("กำลังทำความสะอาดข้อมูล...")
    initial_count = len(df)
    
    # ลบแถวที่มีค่าว่างในคอลัมน์สำคัญ
    df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance'])
    
    # กรองเอาเฉพาะข้อมูลที่ 'ระยะทาง' มากกว่า 0 (กำจัดข้อมูลที่ผิดพลาด)
    df = df[df['trip_distance'] > 0]
    
    print(f"ทำความสะอาดเสร็จสิ้น: จาก {initial_count:,} เหลือ {len(df):,} แถว")

    # 4. ส่งเข้า Database
    print("กำลังส่งข้อมูลเข้า PostgreSQL... โปรดรอสักครู่")
    # เราจะใช้ chunksize เพื่อความเสถียรในการส่งข้อมูลขนาดใหญ่
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace', index=False, chunksize=50000)
    
    t_end = time.time()
    print(f"สำเร็จ ข้อมูลอยู่ใน DB แล้ว (ใช้เวลา: {t_end - t_start:.2f} วินาที)")

if __name__ == '__main__':
    clean_and_ingest('yellow_tripdata_2024-01.parquet')