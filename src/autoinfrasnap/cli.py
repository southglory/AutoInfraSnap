import argparse
from . import collector


def main():
    parser = argparse.ArgumentParser(description="시스템 상태 스냅샷 도구")
    parser.add_argument("--report", action="store_true", help="시스템 상태 리포트 생성")
    parser.add_argument("--output", "-o", help="출력 파일 이름 (기본: 자동 생성)")

    args = parser.parse_args()

    if args.report:
        try:
            info = collector.collect_system_info()
            filename = collector.save_report(info, args.output)
            print(f"리포트가 생성되었습니다: {filename}")
        except Exception as e:
            print(f"에러 발생: {e}")
            return 1
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    main()
