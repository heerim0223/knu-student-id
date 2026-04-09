export default function Footer() {
    return (
        <footer className="mt-auto pb-8 pt-6 text-center text-lg text-slate-400 bg-gray-200">
            <p className="font-bold mb-2 text-slate-500">KNU GYM Application</p>
            <div className="flex flex-col items-center">
                <p>본 앱은 강원대학교 공식 애플리케이션이 아니며,</p>
                <p>컴퓨터공학과 학생이 비공식적으로 개발·운영 중입니다.</p>
            </div>
            <p className="mt-3">건의/문의: <a href="mailto:kim10914@naver.com" className="underline hover:text-sky-500 transition-colors">kim10914@naver.com</a></p>
        </footer>
    );
}
