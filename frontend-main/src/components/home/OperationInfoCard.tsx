import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Clock, Info } from "lucide-react";

interface OperationInfoCardProps {
    isOpen: boolean;
}

export default function OperationInfoCard({ isOpen }: OperationInfoCardProps) {
    return (
        <Card className="shadow-sm border-slate-100 bg-white/90 backdrop-blur-md text-xl">
            <CardHeader className="pb-2">
                <CardTitle className="text-2xl flex justify-between items-center text-slate-800 px-2">
                    <span className="flex items-center gap-2 font-bold">
                        <Clock className="w-5 h-5 text-sky-500" /> 운영 정보
                    </span>
                    {isOpen ? (
                        <Badge className="bg-blue-50 text-blue-600 hover:bg-blue-100 border border-blue-200 pointer-events-none text-lg p-3">
                            운영 중
                        </Badge>
                    ) : (
                        <Badge variant="destructive" className="pointer-events-none text-lg p-3">
                            운영 종료
                        </Badge>
                    )}
                </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
                <div className="flex justify-between items-center p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                    <span className="text-slate-600 font-medium">평일 운영시간</span>
                    <span className="font-bold text-slate-900">12:00 ~ 22:00</span>
                </div>

                <Alert className="mt-1 bg-sky-50 border-sky-100/50 text-sky-900">
                    <Info className="h-5 w-5 text-sky-600" />
                    <AlertTitle className="font-bold text-lg">주말 및 공휴일 휴무</AlertTitle>
                    <AlertDescription className="text-sky-700/80 leading-relaxed mt-1.5 text-lg">
                        헬스장은 평일에만 운영됩니다. 주말과 법정 공휴일은 이용할 수 없으니 방문에 참고해 주시기 바랍니다.
                    </AlertDescription>
                </Alert>
            </CardContent>
        </Card>
    );
}
