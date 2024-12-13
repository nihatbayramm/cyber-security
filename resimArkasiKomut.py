import os
import subprocess

class ImageCommandInjector:
    def __init__(self, image_path, output_path, command):
        self.image_path = image_path
        self.output_path = output_path
        self.command = command

    def inject_command(self):
        with open(self.image_path, "ab") as img:
            img.write(f"\n<!-- {self.command} -->\n".encode())
        print(f"[+] Komut görsele eklendi: {self.output_path}")
        os.rename(self.image_path, self.output_path)

    def extract_and_execute(self):
        with open(self.output_path, "rb") as img:
            content = img.read()
            if b"<!--" in content and b"-->" in content:
                extracted_command = content.split(b"<!--")[1].split(b"-->", 1)[0].decode()
                print(f"[+] Çıkarılan Komut: {extracted_command}")
                print("[*] Komut çalıştırılıyor...\n")
                result = subprocess.getoutput(extracted_command)
                print(result)
            else:
                print("[!] Görselde komut bulunamadı!")

def main():
    image_path = input("Görsel dosyasının yolu: ").strip()
    output_path = "injected_image.png"
    command = input("Çalıştırmak istediğiniz komutu girin: ").strip()
    
    injector = ImageCommandInjector(image_path, output_path, command)
    injector.inject_command()
    input("[*] Komut eklendi. Devam etmek için Enter'a basın...")
    injector.extract_and_execute()

if __name__ == "__main__":
    main()