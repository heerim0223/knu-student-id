import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users } from "lucide-react";

interface CongestionCardProps {
    isOpen: boolean;
    currentPeople: number;
    rawCountText: string;
}

export default function CongestionCard({ isOpen, currentPeople, rawCountText }: CongestionCardProps) {
    // 혼잡도 뱃지 및 색상 로직 처리
    let statusText = "여유";
    let statusColor = "bg-emerald-500 hover:bg-emerald-600";

    if (!isOpen) {
        statusText = "-";
        statusColor = "bg-slate-400 hover:bg-slate-500";
    } else if (currentPeople >= 16) {
        statusText = "혼잡";
        statusColor = "bg-red-500 hover:bg-red-600 text-white";
    } else if (currentPeople >= 9) {
        statusText = "보통";
        statusColor = "bg-amber-400 hover:bg-amber-500 text-black";
    }

    return (
        <Card className="shadow-sm border-slate-100 bg-white/90 backdrop-blur-md px-2">
            <CardHeader>
                <CardTitle className="text-2xl flex justify-between items-center text-slate-800">
                    <span className="flex items-center gap-2 font-bold">
                        <Users className="w-5 h-5 text-sky-500" /> 현재 이용 현황
                    </span>
                    <Badge className={`${statusColor} transition-colors pointer-events-none text-sm px-3 py-1 shadow-sm`}>
                        {statusText}
                    </Badge>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex items-end gap-2">
                    {isOpen ? (
                        <>
                            <span className="text-4xl font-extrabold text-slate-900">{currentPeople}</span>
                            <span className="text-sm font-medium text-slate-500 mb-1">명</span>
                        </>
                    ) : (
                        <span className="text-xl font-bold text-slate-600 my-1">{rawCountText}</span>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
