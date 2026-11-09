"use client";
import { createContext, useContext } from "react";
import type { Socket } from "socket.io-client";

// null while signed out or before the handshake completes - consumers should treat it as "not ready yet".
export const NotificationSocketContext = createContext<Socket | null>(null);

export const useNotificationSocket = (): Socket | null => useContext(NotificationSocketContext);
