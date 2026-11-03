import csv
import os
from datetime import datetime

FILE = "attendance.csv"

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def save(rows):
    with open(FILE, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(rows)

def today():
    return datetime.today().strftime('%Y-%m-%d')

def valid_date(s):
    try:
        datetime.strptime(s, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def register():
    print("\n[ 출석 등록 ]")
    d = input(f"날짜 (YYYY-MM-DD) [Enter = 오늘 {today()}]: ").strip()
    if d == '':
        d = today()
    if not valid_date(d):
        print("❌ 날짜 형식이 올바르지 않습니다.")
        return
    name = input("이름: ").strip()
    if not name:
        print("❌ 이름을 입력해주세요.")
        return
    rows = load()
    if [d, name] in rows:
        print(f"⚠️  이미 등록되어 있습니다. ({d} / {name})")
        return
    rows.append([d, name])
    save(rows)
    print(f"✅ 출석 등록 완료! ({d} / {name})")

def list_all():
    print("\n[ 전체 출석 목록 ]")
    rows = sorted(load())
    if not rows:
        print("  등록된 출석이 없습니다.")
        return
    cur = ''
    for d, name in rows:
        if d != cur:
            print(f"\n  📅 {d}")
            cur = d
        print(f"     ✔ {name}")
    print(f"\n  총 {len(rows)}건")

def search_name():
    print("\n[ 이름으로 검색 ]")
    name = input("검색할 이름: ").strip()
    rows = [r for r in load() if r[1] == name]
    if not rows:
        print(f"  '{name}' 의 출석 기록이 없습니다.")
        return
    print(f"\n  '{name}' 출석 기록 ({len(rows)}회)")
    for d, _ in sorted(rows):
        print(f"     ✔ {d}")

def search_date():
    print("\n[ 날짜로 검색 ]")
    d = input(f"검색할 날짜 (YYYY-MM-DD) [Enter = 오늘 {today()}]: ").strip()
    if d == '':
        d = today()
    if not valid_date(d):
        print("❌ 날짜 형식이 올바르지 않습니다.")
        return
    rows = [r for r in load() if r[0] == d]
    if not rows:
        print(f"  {d} 출석 기록이 없습니다.")
        return
    print(f"\n  📅 {d} 출석자 ({len(rows)}명)")
    for _, name in rows:
        print(f"     ✔ {name}")

def menu():
    while True:
        print("""
===================================
    📋 스터디 출석부 프로그램
===================================

  1. 출석 등록
  2. 전체 목록 보기
  3. 이름으로 검색
  4. 날짜로 검색
  0. 종료
""")
        choice = input("번호를 선택하세요: ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            list_all()
        elif choice == '3':
            search_name()
        elif choice == '4':
            search_date()
        elif choice == '0':
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ 올바른 번호를 입력해주세요.")

if __name__ == '__main__':
    menu()