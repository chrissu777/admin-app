import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Navbar = () => {
  return (
    <nav className="bg-med-gray w-full">
      <div className="px-4 mx-auto flex justify-between items-center">
        <div className="justify-start flex-shrink 0 p-2">
          <Link to="/">
            <div className="bg-whitesmoke p-0.5 rounded">
              <img src={logo} className="h-8 sm:h-6 md:h-8 lg:h-10" />
            </div>
          </Link>
        </div>

        <div className="flex-grow">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-white font-figtree">
                Home
              </Link>
            </li>
            <li>
              <Link to="/recordings" className="text-white font-figtree">
                Recordings
              </Link>
            </li>
          </ul>
        </div>
        <div>
          <text className="text-white">Settings</text>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
