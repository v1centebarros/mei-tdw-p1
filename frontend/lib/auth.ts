import NextAuth from "next-auth"
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
        }
    }
})