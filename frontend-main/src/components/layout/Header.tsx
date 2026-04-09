import { Card } from "@/components/ui/card";
import knuIcon from "@/assets/KNUICON.png";

export default function Header() {
    return (
        <header className="px-4 mt-40 mb-10">
            <Card className="relative overflow-hidden border-none shadow-md bg-linear-to-br from-sky-400 to-sky-500 py-13">
                {/* 디자인용 빛 반사 효과 (우측 상단 원) */}
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/20 rounded-full blur-3xl"></div>

                <div className="flex flex-col items-center gap-3">
                    <img src={knuIcon} alt="강원대 로고" className="w-36" />
                    <h1 className="text-3xl font-bold text-white text-center">
                        강원대학교 헬스장 현황
                    </h1>
                </div>
            </Card>
        </header>
    );
}
