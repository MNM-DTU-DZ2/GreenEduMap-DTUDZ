/*
 * GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
 * Copyright (C) 2025 DTU-DZ2 Team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */


import { Metadata } from "next";
import SignInForm from "@/components/auth/SignInForm";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { useToast } from "@/context/ToastContext";

export const metadata: Metadata = {
  title: "Login | RELIEFLINK",
  description: "Login to your account",
};

export default function LoginPage() {
  // const router = useRouter();
  // const { login } = useAuthStore();
  // const { success, error: showError } = useToast();
  // const [isLogin, setIsLogin] = useState(true);
  // const [loading, setLoading] = useState(false);

  // const [formData, setFormData] = useState({
  //   email: "",
  //   mat_khau: "",
  //   ho_va_ten: "",
  //   so_dien_thoai: "",
  //   vai_tro: "nguoi_dan",
  // });

  // const handleSubmit = async (e: React.FormEvent) => {
  //   e.preventDefault();
  //   setLoading(true);

  //   try {
  //     const response = await fetch("/api/auth", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify({
  //         action: isLogin ? "login" : "register",
  //         ...formData,
  //       }),
  //     });

  //     const data = await response.json();

  //     if (!response.ok) {
  //       throw new Error(data.error || "Xác thực thất bại");
  //     }

  //     login(data.user, data.token);
  //     success(isLogin ? "🎉 Đăng nhập thành công!" : "🎉 Đăng ký thành công!");

  //     // Redirect based on role
  //     const role = data.user.vai_tro;
  //     if (role === "admin") {
  //       router.push("/admin/dashboard");
  //     } else if (role === "tinh_nguyen_vien") {
  //       router.push("/volunteer/dashboard");
  //     } else {
  //       router.push("/citizen/dashboard");
  //     }
  //   } catch (err: any) {
  //     showError(err.message || "Có lỗi xảy ra, vui lòng thử lại!");
  //   } finally {
  //     setLoading(false);
  //   }
  // };
  return <SignInForm />;
}
