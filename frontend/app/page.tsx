import SignIn from "@/components/sign-in";
import {ModeToggle} from "@/components/mode-toggle";

export default function Home() {
    return (<>
            <h1>Hello World!</h1>
            <SignIn/>
            <ModeToggle/>
        </>
    );
}
