import pandas as pd
import requests
import os
from time import sleep

# Đảm bảo thư mục chứa âm thanh tồn tại
sounds_directory = 'sounds'
os.makedirs(sounds_directory, exist_ok=True)

def get_sound_file(text, directory):
    try:
        # Gửi yêu cầu tạo file âm thanh
        response = requests.post(
            'https://api.soundoftext.com/sounds',
            json={
                'engine': 'Google',
                'data': {'text': text, 'voice': 'en-US'}
            },
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        sound_id = response.json().get('id')

        # Chờ file âm thanh sẵn sàng và lấy URL
        file_url = None
        while not file_url:
            sleep(3)  # Đợi 3 giây trước khi thử lại
            sound_status = requests.get(f'https://api.soundoftext.com/sounds/{sound_id}')
            sound_status.raise_for_status()
            status_data = sound_status.json()
            if status_data.get('status') == 'Done':
                file_url = status_data.get('location')
            else:
                print(f'File not ready yet for "{text}", retrying...')

        # Tải file âm thanh về
        file_name = f"{text.replace(' ', '_').replace('/', '_')}.mp3"
        file_path = os.path.join(directory, file_name)
        file_response = requests.get(file_url, stream=True)
        file_response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in file_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'file_path "{file_path}"')
        return file_path

    except requests.RequestException as e:
        print(f"Error processing '{text}': {e}")
        return None

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    output_rows = []

    for index, row in df.iterrows():
        word = row['Word']
        example = row['Example']

        # Xử lý âm thanh cho word
        word_sound_path = get_sound_file(word, sounds_directory)
        # Xử lý âm thanh cho example
        example_sound_path = get_sound_file(example.split(' / ')[0], sounds_directory)  # Lấy phần tiếng Anh trước dấu '/'
        print(f'word_sound_path "{word_sound_path}"')
        print(f'example_sound_path "{example_sound_path}"')
        
        # Tạo nội dung cho các cột trong file CSV đầu ra
        output_rows.append({
            'Word': word,
            'Meaning': row['Meaning'],
            'Example': f"{example}\n[sound:{example_sound_path}]",
            'Pronunciation': f"{row['Pronunciation']}\n[sound:{word_sound_path}]"
        })

    # Tạo DataFrame và lưu vào file CSV
    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(output_csv, index=False)

# Đường dẫn file CSV đầu vào và đầu ra
input_csv = 'anki-new-word.csv'
output_csv = 'output.csv'

process_csv(input_csv, output_csv)
