import { useLocation } from "react-router-dom";
import ProfileAvatar from "./ProfileAvatar";

const BaseLayout = ({ children }) => {
  const location = useLocation();
  const hideProfileAvatarPaths = ['/login', '/register'];

  return (
    <div className="Form">
      {!hideProfileAvatarPaths.includes(location.pathname) && <ProfileAvatar />}

      <a href="http://127.0.0.1:8080"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F013%2F923%2F542%2Flarge_2x%2Fred-vehicle-car-logo-png.png&f=1&nofb=1&ipt=6d49db9b70b31f8aae08b84219e82077c56756916ccaef12beeabd7f1cc65633" width="100" height="75"></img></a>
      {children}
    </div>
  );
};

export default BaseLayout;