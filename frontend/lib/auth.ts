import NextAuth, {NextAuthConfig} from "next-auth"
import Keycloak from "next-auth/providers/keycloak"

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [Keycloak],
    session: {
        maxAge: 60 * 30
    },
    callbacks: {
        async jwt({ token, account }) {
            if (account) {
                token.idToken = account.id_token
                token.accessToken = account.access_token
                token.refreshToken = account.refresh_token
                token.expiresAt = account.expires_at
            }
            return token

        },
        async session({ session, token }) {
            session.user.accessToken = token.accessToken
            return session
        },
        async authorized({auth,request:{nextUrl}}) {
            const isLoggedIn = !!auth?.user;
            const isOnHome = nextUrl.pathname === '/';

            if (!isOnHome) {
                return isLoggedIn;
            }

            if (isLoggedIn && isOnHome) {
                return Response.redirect(new URL('/dashboard', nextUrl));
            }
            return true;
        },
    }
} satisfies NextAuthConfig)