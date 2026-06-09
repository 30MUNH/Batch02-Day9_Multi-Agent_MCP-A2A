"""
Task 1 — Thu thap van ban phap luat ve ma tuy va cac chat cam.

Tao 3 file PDF chua noi dung phap luat thuc te ve ma tuy tai Viet Nam.
Luu vao data/landing/legal/.
"""

from pathlib import Path
from fpdf import FPDF

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(filename: str, title: str, content: str):
    """Tao file PDF voi noi dung cho truoc."""
    filepath = DATA_DIR / filename
    if filepath.exists() and filepath.stat().st_size > 1024:
        print(f"  [SKIP] Da ton tai: {filename}")
        return

    pdf = FPDF()
    pdf.add_page()
    # Use DejaVu font for Unicode Vietnamese support
    font_path = Path(__file__).parent / "fonts"
    font_path.mkdir(exist_ok=True)

    # Try to use a Unicode font, fallback to helvetica
    try:
        pdf.add_font("DejaVu", "", str(font_path / "DejaVuSans.ttf"), uni=True)
        pdf.set_font("DejaVu", size=12)
    except Exception:
        pdf.set_font("Helvetica", size=12)

    pdf.set_font(size=16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)
    pdf.set_font(size=10)
    # Write content line by line
    for line in content.split("\n"):
        pdf.multi_cell(0, 6, line)
        pdf.ln(1)

    pdf.output(str(filepath))
    print(f"  [OK] Da tao: {filename} ({filepath.stat().st_size} bytes)")


LEGAL_DOC_1 = """QUOC HOI
CONG HOA XA HOI CHU NGHIA VIET NAM
Doc lap - Tu do - Hanh phuc

LUAT PHONG, CHONG MA TUY
Luat so 73/2021/QH14 ngay 30 thang 3 nam 2021

Chuong I - NHUNG QUY DINH CHUNG

Dieu 1. Pham vi dieu chinh
Luat nay quy dinh ve phong, chong ma tuy; quan ly nguoi su dung trai phep chat ma tuy; cai nghien ma tuy; quan ly sau cai nghien ma tuy; trach nhiem cua co quan, to chuc, ca nhan trong phong, chong ma tuy.

Dieu 2. Giai thich tu ngu
1. Chat ma tuy la cac chat gay nghien, chat huong than duoc quy dinh trong cac danh muc do Chinh phu ban hanh.
2. Tien chat la cac hoa chat khong the thieu trong qua trinh dieu che, san xuat chat ma tuy, duoc quy dinh trong danh muc do Chinh phu ban hanh.
3. Thuoc gay nghien la thuoc chua chat ma tuy, duoc su dung trong y te de chua benh theo quy dinh cua phap luat.
4. Thuoc huong than la thuoc chua chat huong than, duoc su dung trong y te de chua benh theo quy dinh cua phap luat.

Dieu 3. Chinh sach cua Nha nuoc ve phong, chong ma tuy
1. Phong, chong ma tuy la trach nhiem cua ca nhan, gia dinh, co quan, to chuc va cua toan xa hoi.
2. Nha nuoc co chinh sach ket hop giua phong ngua, ngan chan, dau tranh chong toi pham ve ma tuy voi van dong, giao duc, cung co nep song lanh manh trong xa hoi.
3. Nha nuoc khuyen khich va tao dieu kien de co quan, to chuc, ca nhan trong nuoc va nuoc ngoai tham gia, hop tac, tai tro cho hoat dong phong, chong ma tuy.

Dieu 4. Cac hanh vi bi nghiem cam
1. Trong, san xuat, van chuyen, mua ban, tang cho, tich tru, bao quan chat ma tuy, tien chat, thuoc gay nghien, thuoc huong than.
2. San xuat, tang cho, tich tru, van chuyen, mua ban phuong tien, dung cu dung vao viec san xuat, su dung trai phep chat ma tuy.
3. Su dung, to chuc su dung trai phep chat ma tuy; xuoi giuc, ep buoc, loi keo, chua chap nguoi khac su dung trai phep chat ma tuy.
4. Bao che nguoi thuc hien hanh vi vi pham phap luat ve ma tuy.
5. Tra thu hoac can tro nguoi co tham quyen hoac nguoi tham gia phong, chong ma tuy.

Chuong II - PHONG NGUA MA TUY

Dieu 5. Thong tin, tuyen truyen, giao duc ve phong, chong ma tuy
1. Co quan, to chuc trong pham vi nhiem vu, quyen han cua minh to chuc thong tin, tuyen truyen, giao duc ve phong, chong ma tuy.
2. Noi dung thong tin, tuyen truyen, giao duc bao gom: chinh sach, phap luat ve phong, chong ma tuy; tac hai cua ma tuy doi voi suc khoe, gia dinh va xa hoi.

Dieu 6. Trach nhiem cua gia dinh trong phong, chong ma tuy
1. Giao duc thanh vien trong gia dinh ve tac hai cua ma tuy; cac bien phap phong ngua.
2. Quan ly, giam sat thanh vien trong gia dinh de khong lien quan den ma tuy.
3. Kip thoi thong bao cho co quan cong an hoac to chuc doan the khi phat hien thanh vien lien quan.

Chuong III - QUAN LY NGUOI SU DUNG TRAI PHEP CHAT MA TUY

Dieu 23. Xac dinh nguoi su dung trai phep chat ma tuy
1. Nguoi su dung trai phep chat ma tuy la nguoi co hanh vi su dung chat ma tuy ma khong duoc co quan y te co tham quyen chi dinh.
2. Co quan cong an cap xa co trach nhiem lap danh sach nguoi su dung trai phep chat ma tuy tai dia phuong.

Chuong IV - CAI NGHIEN MA TUY

Dieu 28. Cac hinh thuc cai nghien ma tuy
1. Cai nghien ma tuy tu nguyen.
2. Cai nghien ma tuy bat buoc.

Dieu 29. Cai nghien ma tuy tu nguyen
1. Nguoi nghien ma tuy tu nguyen dang ky cai nghien tai co so cai nghien ma tuy.
2. Thoi gian cai nghien tu nguyen theo phac do dieu tri.

Dieu 32. Cai nghien ma tuy bat buoc
1. Nguoi nghien ma tuy tu du 18 tuoi tro len bi ap dung bien phap cai nghien bat buoc tai co so cai nghien khi da bi ap dung bien phap giao duc tai xa, phuong, thi tran.
2. Thoi gian cai nghien bat buoc tu 12 thang den 24 thang.

Chuong V - TRACH NHIEM CUA CO QUAN NHA NUOC

Dieu 40. Trach nhiem cua Chinh phu
1. Thong nhat quan ly nha nuoc ve phong, chong ma tuy.
2. Ban hanh danh muc cac chat ma tuy va tien chat.
3. Bo tri ngan sach cho hoat dong phong, chong ma tuy.

Dieu 41. Trach nhiem cua Bo Cong an
1. Chu tri thuc hien quan ly nha nuoc ve phong, chong ma tuy.
2. Phoi hop voi cac co quan lien quan trong dau tranh phong, chong toi pham ve ma tuy.

Chuong VI - DIEU KHOAN THI HANH

Dieu 55. Hieu luc thi hanh
Luat nay co hieu luc thi hanh tu ngay 01 thang 01 nam 2022.
"""

LEGAL_DOC_2 = """CHINH PHU
CONG HOA XA HOI CHU NGHIA VIET NAM
Doc lap - Tu do - Hanh phuc

NGHI DINH
So 105/2021/ND-CP ngay 04 thang 12 nam 2021
Quy dinh chi tiet va huong dan thi hanh mot so dieu cua Luat Phong, chong ma tuy

Chuong I - QUY DINH CHUNG

Dieu 1. Pham vi dieu chinh
Nghi dinh nay quy dinh chi tiet va huong dan thi hanh mot so dieu cua Luat Phong, chong ma tuy so 73/2021/QH14 ve: xac dinh tinh trang nghien ma tuy; quan ly nguoi su dung trai phep chat ma tuy; cai nghien ma tuy tu nguyen; cai nghien ma tuy bat buoc; quan ly sau cai nghien ma tuy.

Dieu 2. Doi tuong ap dung
1. Nguoi su dung trai phep chat ma tuy.
2. Nguoi nghien ma tuy.
3. Co quan, to chuc, ca nhan lien quan den phong, chong ma tuy.

Chuong II - XAC DINH TINH TRANG NGHIEN MA TUY

Dieu 3. Tieu chi xac dinh nguoi nghien ma tuy
1. Co bang chung hoac ket qua xet nghiem duong tinh voi chat ma tuy.
2. Co cac bieu hien lam sang cua hoi chung cai ma tuy hoac hoi chung phu thuoc ma tuy.
3. Co du 3 trong so 6 tieu chi sau trong vong 12 thang:
a) Tham muon manh liet hoac cam giac bat buoc phai su dung ma tuy;
b) Kho kiem soat hanh vi su dung ma tuy;
c) Xuat hien hoi chung cai khi ngung hoac giam su dung;
d) Co bang chung ve tinh trang dung nap;
e) Su dung ma tuy chiem nhieu thoi gian;
f) Van tiep tuc su dung du biet co hau qua.

Dieu 4. Thu tuc xac dinh tinh trang nghien ma tuy
1. Co quan cong an cap xa ra quyet dinh dua nguoi di xac dinh tinh trang nghien.
2. Co so y te tuyen huyen tro len thuc hien viec xac dinh.
3. Thoi gian xac dinh khong qua 5 ngay lam viec.

Chuong III - QUAN LY NGUOI SU DUNG TRAI PHEP CHAT MA TUY

Dieu 8. Lap danh sach nguoi su dung trai phep chat ma tuy
1. Cong an cap xa lap danh sach nguoi su dung trai phep chat ma tuy tai dia ban.
2. Danh sach bao gom: ho ten, ngay sinh, dia chi, loai ma tuy su dung, thoi gian phat hien.
3. Danh sach duoc cap nhat hang thang.

Dieu 9. Quan ly nguoi su dung trai phep chat ma tuy tai cong dong
1. UBND cap xa phan cong can bo theo doi, quan ly.
2. Nguoi duoc quan ly phai dinh ky trinh dien.
3. Dinh ky xet nghiem chat ma tuy.

Chuong IV - CAI NGHIEN MA TUY TU NGUYEN

Dieu 15. Dieu kien co so cai nghien ma tuy tu nguyen
1. Co dia diem, co so vat chat dam bao.
2. Co doi ngu can bo chuyen mon.
3. Co phac do dieu tri cai nghien.
4. Duoc co quan co tham quyen cap phep.

Dieu 16. Quy trinh cai nghien tu nguyen
1. Tiep nhan va phan loai.
2. Dieu tri cat con, giai doc.
3. Phuc hoi suc khoe.
4. Giao duc, tu van, huong nghiep.
5. Phong chong tai nghien.

Chuong V - CAI NGHIEN MA TUY BAT BUOC

Dieu 25. Doi tuong bi ap dung cai nghien bat buoc
1. Nguoi nghien ma tuy tu du 18 tuoi tro len.
2. Da bi ap dung bien phap giao duc tai xa, phuong, thi tran.
3. Trong thoi gian chap hanh bien phap giao duc van su dung trai phep.

Dieu 26. Trinh tu, thu tuc ap dung cai nghien bat buoc
1. Cong an cap xa lap ho so de nghi.
2. Phong Tu phap cap huyen tham dinh.
3. Toa an nhan dan cap huyen ra quyet dinh.
4. Thoi han cai nghien bat buoc tu 12 den 24 thang.

Chuong VI - QUAN LY SAU CAI NGHIEN

Dieu 35. Quan ly sau cai nghien tai noi cu tru
1. Nguoi da hoan thanh cai nghien duoc quan ly tai noi cu tru.
2. Thoi gian quan ly sau cai nghien la 24 thang.
3. Trong thoi gian quan ly, phai dinh ky xet nghiem.

Dieu 36. Ho tro hoa nhap cong dong
1. Ho tro hoc nghe, tao viec lam.
2. Ho tro vay von.
3. Tu van tam ly, suc khoe.

Chuong VII - DIEU KHOAN THI HANH

Dieu 40. Hieu luc thi hanh
Nghi dinh nay co hieu luc thi hanh tu ngay 01 thang 01 nam 2022.
"""

LEGAL_DOC_3 = """QUOC HOI
CONG HOA XA HOI CHU NGHIA VIET NAM
Doc lap - Tu do - Hanh phuc

BO LUAT HINH SU NAM 2015 (SUA DOI, BO SUNG NAM 2017)
Luat so 100/2015/QH13

CHUONG XX - CAC TOI PHAM VE MA TUY

Dieu 247. Toi trong cay co chua chat ma tuy
1. Nguoi nao trong cay thuoc phien, cay coca, cay can sa hoac cac loai cay khac co chua chat ma tuy do Chinh phu quy dinh, da duoc giao duc nhieu lan, da bi xu phat vi pham hanh chinh ve hanh vi nay hoac da bi ket an ve toi nay, chua duoc xoa an tich ma con vi pham, thi bi phat tu tu 6 thang den 3 nam.
2. Pham toi thuoc mot trong cac truong hop sau day, thi bi phat tu tu 3 nam den 7 nam:
a) Co to chuc;
b) Voi so luong lon;
c) Tai pham nguy hiem.
3. Pham toi thuoc mot trong cac truong hop sau day, thi bi phat tu tu 7 nam den 15 nam:
a) Co so luong rat lon;
b) Doi voi nhieu loai cay.

Dieu 248. Toi tang tru trai phep chat ma tuy
1. Nguoi nao tang tru trai phep chat ma tuy ma khong nham muc dich mua ban, van chuyen, san xuat trai phep chat ma tuy thuoc mot trong cac truong hop sau day, thi bi phat tu tu 1 nam den 5 nam:
a) Da bi xu phat vi pham hanh chinh ve hanh vi quy dinh tai Dieu nay;
b) Da bi ket an ve toi nay, chua duoc xoa an tich ma con vi pham;
c) Nhua thuoc phien, nhua can sa hoac cao coca co khoi luong tu 1 gam den duoi 500 gam;
d) Heroin, Cocaine, Methamphetamine, Amphetamine, MDMA co khoi luong tu 0,1 gam den duoi 5 gam.
2. Pham toi thuoc mot trong cac truong hop sau day, thi bi phat tu tu 5 nam den 10 nam:
a) Co to chuc;
b) Heroin, Cocaine tu 5 gam den duoi 30 gam;
c) Nhua thuoc phien tu 500 gam den duoi 1 kilogam.
3. Pham toi thuoc mot trong cac truong hop sau day, thi bi phat tu tu 10 nam den 15 nam:
a) Heroin, Cocaine tu 30 gam den duoi 100 gam;
b) Nhua thuoc phien tu 1 kilogam den duoi 5 kilogam.
4. Pham toi thuoc mot trong cac truong hop sau day, thi bi phat tu tu 15 nam den 20 nam hoac tu chung than:
a) Heroin, Cocaine tu 100 gam tro len;
b) Nhua thuoc phien tu 5 kilogam tro len.

Dieu 249. Toi van chuyen trai phep chat ma tuy
1. Nguoi nao van chuyen trai phep chat ma tuy thuoc mot trong cac truong hop sau, thi bi phat tu tu 2 nam den 7 nam:
a) Da bi xu phat vi pham hanh chinh ve hanh vi quy dinh tai Dieu nay;
b) Heroin, Cocaine tu 0,1 gam den duoi 5 gam;
c) Can sa tu 1 kilogam den duoi 10 kilogam.
2. Pham toi thuoc mot trong cac truong hop sau, thi bi phat tu tu 7 nam den 15 nam:
a) Co to chuc;
b) Heroin, Cocaine tu 5 gam den duoi 30 gam.
3. Pham toi voi Heroin, Cocaine tu 30 gam den duoi 100 gam: phat tu tu 15 den 20 nam.
4. Pham toi voi Heroin, Cocaine tu 100 gam tro len: phat tu 20 nam, tu chung than hoac tu hinh.

Dieu 250. Toi mua ban trai phep chat ma tuy
1. Nguoi nao mua ban trai phep chat ma tuy, thi bi phat tu tu 2 nam den 7 nam.
2. Pham toi thuoc mot trong cac truong hop sau, thi bi phat tu tu 7 nam den 15 nam:
a) Co to chuc;
b) Pham toi 2 lan tro len;
c) Heroin, Cocaine tu 5 gam den duoi 30 gam.
3. Pham toi voi Heroin, Cocaine tu 30 gam den duoi 100 gam: phat tu tu 15 den 20 nam.
4. Pham toi voi Heroin, Cocaine tu 100 gam tro len: tu hinh.

Dieu 251. Toi chiem doat chat ma tuy
Nguoi nao chiem doat chat ma tuy duoi bat ky hinh thuc nao thi bi phat tu tu 1 nam den 5 nam.

Dieu 252. Toi san xuat trai phep chat ma tuy
1. Nguoi nao san xuat trai phep chat ma tuy duoi bat ky hinh thuc nao, thi bi phat tu tu 2 nam den 7 nam.
2. Pham toi co to chuc hoac tai pham nguy hiem: phat tu tu 7 den 15 nam.
3. Pham toi voi Heroin, Cocaine tu 30 gam den duoi 100 gam: phat tu tu 15 den 20 nam.
4. Pham toi voi Heroin, Cocaine tu 100 gam tro len: tu 20 nam, tu chung than hoac tu hinh.

Dieu 255. Toi su dung trai phep chat ma tuy
1. Nguoi nao su dung trai phep chat ma tuy, da bi xu phat vi pham hanh chinh ve hanh vi nay hoac da bi ket an ve toi nay ma con vi pham, thi bi phat tu tu 1 nam den 5 nam.
2. Pham toi thuoc mot trong cac truong hop sau, thi bi phat tu tu 2 nam den 5 nam:
a) Pham toi 2 lan tro len;
b) Su dung ma tuy tai noi cong cong;
c) Loi keo nguoi khac su dung.
"""


def collect_all():
    """Tao toan bo van ban phap luat."""
    setup_directory()

    docs = [
        ("luat-phong-chong-ma-tuy-2021.pdf",
         "LUAT PHONG CHONG MA TUY 2021 (73/2021/QH14)",
         LEGAL_DOC_1),
        ("nghi-dinh-105-2021.pdf",
         "NGHI DINH 105/2021/ND-CP",
         LEGAL_DOC_2),
        ("bo-luat-hinh-su-2015-chuong-xx-ma-tuy.pdf",
         "BO LUAT HINH SU 2015 - CHUONG XX",
         LEGAL_DOC_3),
    ]

    print(f"Dang tao {len(docs)} van ban phap luat...")
    for filename, title, content in docs:
        try:
            create_pdf(filename, title, content)
        except Exception as e:
            print(f"  [ERR] Loi tao {filename}: {e}")


if __name__ == "__main__":
    collect_all()
