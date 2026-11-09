import { redirect } from "next/navigation";

const ModerationPage = () => {
    redirect("/pm/moderation/resources/pending");
};

export default ModerationPage;
