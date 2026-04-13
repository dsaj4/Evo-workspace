import pandas as pd
import os

# 读取 CSV 文件
csv_path = r'E:\Project\论文\workspace\eventdatabase\AI 事件数据库_v2.0_20260330.CSV'
print(f'检查文件：{csv_path}')
print(f'文件存在：{os.path.exists(csv_path)}')

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8')
    print(f'\n数据形状：{df.shape}')
    print(f'\n列名：{df.columns.tolist()}')
    print(f'\n前 10 行:')
    print(df.head(10).to_string())
    print(f'\n事件类型统计:')
    print(df['event_type'].value_counts())
else:
    print('文件不存在，尝试读取 PDF...')
    # 尝试读取 PDF
    try:
        import fitz
        pdf_path = r'E:\Project\论文\workspace\eventdatabase\AI 技术积极事件调研.pdf'
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
        print('\nPDF 内容:')
        print(text[:2000])
    except Exception as e:
        print(f'读取 PDF 失败：{e}')
