import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import CongestionCard from "@/components/home/CongestionCard";
import OperationInfoCard from "@/components/home/OperationInfoCard";
import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface StatusData {
    isOpen: boolean;
    currentPeople: number;
    rawCountText: string;
}

export default function Home() {
    const [statusData, setStatusData] = useState<StatusData>({
        isOpen: false,
        currentPeople: 0,
        rawCountText: "로딩 중..."
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/status');
                if (response.ok) {
                    const data = await response.json();
                    setStatusData(data);
                } else {
                    console.error('API 요청 실패');
                }
            } catch (error) {
                console.error('API 연결 실패:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStatus();
        // 5초마다 업데이트
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col h-full bg-sky-200">
                <Header />
                <main className="flex flex-col gap-4 px-4 grow justify-center items-center">
                    <div className="text-xl">로딩 중...</div>
                </main>
                <Footer />
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full bg-sky-200">
            {/* 1. 공통 헤더 */}
            <Header />
            <main className="flex flex-col gap-4 px-4 grow">
                {/* 2. 혼잡도 카드 */}
                <CongestionCard
                    isOpen={statusData.isOpen}
                    currentPeople={statusData.currentPeople}
                    rawCountText={statusData.rawCountText}
                />

                {/* 3. 운영 정보 카드 */}
                <OperationInfoCard isOpen={statusData.isOpen} />
            </main>

            {/* 4. 공통 푸터 */}
            <Footer />
        </div>
    );
}