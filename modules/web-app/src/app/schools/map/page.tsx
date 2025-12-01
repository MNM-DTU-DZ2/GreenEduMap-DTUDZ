import SchoolMap from "@/components/map/SchoolMap";

export default function SchoolMapPage() {
    return (
        <div className="flex flex-col h-screen w-full">
            <div className="flex-1 relative">
                <SchoolMap />
            </div>
        </div>
    );
}
