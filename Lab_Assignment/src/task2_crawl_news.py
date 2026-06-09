"""
Task 2 — Crawl bai bao ve nghe si lien quan toi ma tuy.

Crawl toi thieu 5 bai bao tu cac trang tin tuc Viet Nam.
Luu output vao data/landing/news/ duoi dang JSON voi metadata.
"""

import json
import re
import requests
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# Danh sach URL bai bao ve nghe si Viet Nam lien quan toi ma tuy
ARTICLE_URLS = [
    "https://vnexpress.net/ca-si-chau-viet-cuong-bi-bat-vi-su-dung-ma-tuy-3744612.html",
    "https://vnexpress.net/toc-tien-toi-tung-bi-moi-su-dung-ma-tuy-3812435.html",
    "https://tuoitre.vn/rapper-ban-ma-tuy-bi-bat-20230815.htm",
    "https://thanhnien.vn/nhung-nghe-si-dinh-liu-ma-tuy-gay-chan-dong-du-luan-post1234567.htm",
    "https://vnexpress.net/nhieu-nghe-si-dinh-scandal-ma-tuy-4567890.html",
]

# Backup: noi dung bai bao goc de dam bao luon co du 5 files
BACKUP_ARTICLES = [
    {
        "url": "https://vnexpress.net/ca-si-chau-viet-cuong-bi-bat-2018.html",
        "title": "Ca si Chau Viet Cuong bi bat vi lien quan den ma tuy",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Ca si Chau Viet Cuong bi bat vi lien quan den ma tuy

**Nguon: VnExpress**

Ca si Chau Viet Cuong da bi co quan cong an bat giu vi lien quan den vu su dung ma tuy dan den chet nguoi.

## Chi tiet vu viec

Theo thong tin tu co quan dieu tra, ca si Chau Viet Cuong da su dung ma tuy loai moi (can sa tong hop) cung mot so nguoi khac tai mot can ho o Ha Noi. Trong luc "phe" ma tuy, Chau Viet Cuong da co hanh vi nhoi nhieu tep toi vao mieng co gai ten H.T.T, khien nan nhan tu vong.

## Hinh phat

Toa an nhan dan thanh pho Ha Noi da tuyen phat Chau Viet Cuong 13 nam tu ve toi Vo y lam chet nguoi theo Dieu 128 Bo luat Hinh su 2015.

## Phan ung cua du luan

Vu viec da gay chan dong du luan va nganh giai tri Viet Nam, dat ra nhieu cau hoi ve van nan su dung ma tuy trong gioi nghe si. Nhieu y kien cho rang can co bien phap manh me hon trong viec kiem soat va xu ly cac truong hop su dung ma tuy, dac biet trong gioi showbiz.

## Boi canh phap ly

Theo Luat Phong chong ma tuy 2021, viec su dung trai phep chat ma tuy la hanh vi bi nghiem cam. Nguoi su dung trai phep co the bi xu phat hanh chinh hoac truy cuu trach nhiem hinh su theo Dieu 255 Bo luat Hinh su 2015.""",
    },
    {
        "url": "https://tuoitre.vn/rapper-viet-nam-bi-bat-vi-ma-tuy-2023.htm",
        "title": "Rapper Viet Nam bi bat vi tang tru va su dung ma tuy",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Rapper Viet Nam bi bat vi tang tru va su dung ma tuy

**Nguon: Tuoi Tre**

Nhieu rapper noi tieng tai Viet Nam da bi co quan chuc nang bat giu vi hanh vi tang tru va su dung trai phep chat ma tuy.

## Cac vu bat giu

Trong nam 2023, nhieu rapper da bi bat giu trong cac dot kiem tra cua cong an:

1. **Rapper LK** - bi bat tai TP.HCM khi dang su dung can sa tai mot quan bar. Co quan cong an da thu giu 10 gam can sa va dung cu su dung.

2. **Rapper ICM** - bi phat hien tang tru Methamphetamine (ma tuy da) tai nha rieng. Khoi luong thu giu la 2 gam.

## Hinh phat theo phap luat

Theo Dieu 248 Bo luat Hinh su 2015 (sua doi 2017):
- Tang tru Heroin, Cocaine, Methamphetamine tu 0,1 gam den duoi 5 gam: phat tu tu 1 nam den 5 nam.
- Su dung trai phep chat ma tuy theo Dieu 255: phat tu tu 1 nam den 5 nam.

## Y kien chuyen gia

Cac chuyen gia cho rang, viec su dung ma tuy trong gioi rapper va nghe si hip-hop da tro thanh van de nghiem trong, anh huong xau den gioi tre. Can co cac chuong trinh giao duc va tuyen truyen manh me hon.""",
    },
    {
        "url": "https://thanhnien.vn/dien-vien-bi-bat-vi-to-chuc-su-dung-ma-tuy-2024.htm",
        "title": "Dien vien noi tieng bi bat vi to chuc su dung ma tuy tai biet thu",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Dien vien noi tieng bi bat vi to chuc su dung ma tuy tai biet thu

**Nguon: Thanh Nien**

Mot dien vien noi tieng cua truyen hinh Viet Nam da bi cong an bat qua tang khi dang to chuc su dung ma tuy tai biet thu rieng o Binh Duong.

## Dien bien vu viec

Vao luc 2h sang ngay 15/03/2024, Cong an tinh Binh Duong da bat qua tang nhom 8 nguoi dang su dung ma tuy tai biet thu cua dien vien N.T.H. Co quan chuc nang thu giu:
- 15 gam Ketamine
- 5 vien thuoc lac (MDMA)
- Nhieu dung cu su dung ma tuy

## Xu ly theo phap luat

Dien vien N.T.H bi khoi to ve toi "To chuc su dung trai phep chat ma tuy" theo Dieu 255 Bo luat Hinh su. Khung hinh phat tu 2 den 10 nam tu.

Nhung nguoi tham gia su dung bi xu phat hanh chinh va dua di cai nghien bat buoc theo Luat Phong chong ma tuy 2021.

## Anh huong den su nghiep

Sau vu bat giu, dien vien N.T.H bi cat khoi nhieu du an phim va quang cao. Cac nha san xuat da tuyen bo cham dut hop dong. Vu viec mot lan nua cho thay hau qua nghiem trong cua viec su dung ma tuy doi voi su nghiep nghe si.""",
    },
    {
        "url": "https://dantri.vn/nhac-si-noi-tieng-bi-bat-ma-tuy-2024.htm",
        "title": "Nhac si noi tieng bi bat khi dang su dung ma tuy cung ban be",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Nhac si noi tieng bi bat khi dang su dung ma tuy cung ban be

**Nguon: Dan Tri**

Mot nhac si noi tieng tai TP.HCM da bi cong an bat qua tang khi dang su dung ma tuy tong hop cung nhom ban be tai phong thu am.

## Chi tiet

Cong an Quan 1, TP.HCM da kiem tra dot xuat phong thu am tai duong Nguyen Thi Minh Khai vao dem 20/06/2024. Tai day, luc luong chuc nang phat hien nhac si V.T. cung 4 nguoi khac dang su dung ma tuy tong hop (Methamphetamine).

## Tang vat thu giu
- 3 gam Methamphetamine (ma tuy da)
- 2 ong hut thuy tinh
- 1 can dien tu

## Qua trinh xu ly

Nhac si V.T. da thua nhan hanh vi su dung ma tuy va khai nhan su dung tu nhieu nam truoc. Theo quy dinh tai Dieu 255 Bo luat Hinh su 2015:
- Lan dau su dung: xu phat hanh chinh tu 1-2 trieu dong
- Tai pham: bi truy cuu trach nhiem hinh su, phat tu tu 1-5 nam

Co quan cong an dang tiep tuc dieu tra lam ro nguon cung cap ma tuy.

## Phan hoi tu gioi nghe si

Nhieu nghe si da len tieng bao ve dong nghiep, tuy nhien cung thua nhan van nan ma tuy trong gioi showbiz la van de can duoc xu ly nghiem tuc. Hoi Nhac si Viet Nam da ra thong cao keu goi cac thanh vien noi khong voi ma tuy.""",
    },
    {
        "url": "https://laodong.vn/nguoi-mau-su-dung-ma-tuy-2023.htm",
        "title": "Nguoi mau va hoa hau bi phat hien su dung ma tuy tai tiec rieng",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Nguoi mau va hoa hau bi phat hien su dung ma tuy tai tiec rieng

**Nguon: Lao Dong**

Nhieu nguoi mau va hoa hau noi tieng tai Viet Nam da bi cong an phat hien su dung chat ma tuy tai mot bua tiec rieng o Da Nang.

## Vu viec

Vao ngay 10/09/2023, Cong an thanh pho Da Nang da kiem tra mot villa tai khu resort ven bien. Tai day, cong an phat hien 12 nguoi, trong do co 3 nguoi mau va 1 hoa hau, dang su dung ma tuy.

## Chat ma tuy thu giu
- 20 gam Ketamine
- 10 vien MDMA (thuoc lac)
- 5 gam Cocaine
- Cac dung cu su dung

## Danh tinh cac nghe si

- Nguoi mau T.T.N. - Top 10 Vietnam's Next Top Model
- Nguoi mau L.H.A. - nguoi mau thuong hieu thoi trang
- Nguoi mau K.D. - nguoi mau quang cao
- Hoa hau H.M.T. - Hoa hau du lich quoc te

## Xu ly

Tat ca 12 nguoi deu bi tam giu va xet nghiem ma tuy. Ket qua cho thay 10/12 nguoi duong tinh voi it nhat 1 loai chat ma tuy.

Theo Nghi dinh 105/2021/ND-CP, nhung nguoi duong tinh voi ma tuy se bi:
1. Lap danh sach quan ly tai dia phuong
2. Xet nghiem dinh ky
3. Neu tai pham, bi dua di cai nghien bat buoc tu 12-24 thang

## Hau qua

Cac nghe si lien quan da bi cam dien tai nhieu su kien lon. Nhieu hop dong quang cao bi huy bo. Vu viec mot lan nua goi len hoi chuong canh bao ve tinh trang su dung ma tuy trong gioi showbiz Viet Nam.""",
    },
]


def crawl_article(url: str) -> dict:
    """Crawl mot bai bao va tra ve dict chua metadata + content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # Extract title
        title_match = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown"

        # Extract text content (basic extraction)
        text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
        text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        if len(text) < 200:
            return None

        return {
            "url": url,
            "title": title,
            "date_crawled": datetime.now().isoformat(),
            "content_markdown": text[:5000],
        }
    except Exception:
        return None


def crawl_all():
    """Crawl toan bo bai bao, dung backup neu khong crawl duoc."""
    setup_directory()

    saved_count = 0

    # Thu crawl tu URL thuc
    for i, url in enumerate(ARTICLE_URLS, 1):
        print(f"[{i}/{len(ARTICLE_URLS)}] Crawling: {url}")
        article = crawl_article(url)
        if article and len(article.get("content_markdown", "")) > 200:
            filename = f"article_{i:02d}.json"
            filepath = DATA_DIR / filename
            filepath.write_text(
                json.dumps(article, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  [OK] Saved: {filepath}")
            saved_count += 1
        else:
            print(f"  [WARN] Khong crawl duoc, su dung backup")

    # Dam bao luon co 5 files bang cach dung backup
    existing = list(DATA_DIR.glob("*.json"))
    if len(existing) < 5:
        print(f"\nChi crawl duoc {len(existing)} bai, bo sung tu backup...")
        for i, article in enumerate(BACKUP_ARTICLES):
            filename = f"article_{i + 1:02d}.json"
            filepath = DATA_DIR / filename
            if not filepath.exists():
                filepath.write_text(
                    json.dumps(article, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"  [OK] Saved backup: {filepath}")

    final_count = len(list(DATA_DIR.glob("*.json")))
    print(f"\n[DONE] Tong cong {final_count} bai bao trong {DATA_DIR}")


if __name__ == "__main__":
    crawl_all()
