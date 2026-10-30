
import type { Metadata } from "next";
import { Providers } from "@/app/providers";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Hub Brasil | O Brasil acontece. O povo precisa entender.",
    template: "%s | Hub Brasil"
  },
  description:
    "Informação pública explicada em linguagem acessível. Entenda o que acontece no Brasil e como isso afeta sua vida.",
  applicationName: "Hub Brasil"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
