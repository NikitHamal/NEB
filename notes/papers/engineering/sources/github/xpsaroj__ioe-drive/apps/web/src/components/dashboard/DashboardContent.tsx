import { JumpBackIn } from "@/components/common/resources";

import DashboardActions from "./DashboardActions";
import DashboardHero from "./DashboardHero";
import SemesterInformation from "./SemesterInformation";
import WeeklySummary from "./WeeklySummary";

const DashboardContent = () => {
  return (
    <div className="space-y-8">
      <DashboardHero />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <JumpBackIn fillHeight />
        </div>
        <WeeklySummary />
      </div>

      <DashboardActions />
      <SemesterInformation />
    </div>
  );
};

export default DashboardContent;
