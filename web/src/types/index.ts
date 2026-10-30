export interface Student {
  id: number;
  name: string;
  phone: string;
  roll?: string;
  batch?: string;
  whatsappStatus: 'active' | 'inactive' | 'unknown';
  consentStatus: 'granted' | 'unknown' | 'revoked';
  notes?: string;
}

export interface Template {
  id: number;
  title: string;
  category: string;
  variants: string[];
  updatedAt: string;
}

export interface CampaignRecipient {
  id: number;
  studentId: number;
  name: string;
  phone: string;
  variantIndex: number;
  smsVariant: string;
  personalizedMessage: string;
  status: 'pending' | 'sent' | 'skipped' | 'failed';
  errorMessage?: string;
  sentAt?: string;
}

export interface Campaign {
  id: number;
  name: string;
  createdAt: string;
  totalRecipients: number;
  sentCount: number;
  skippedCount: number;
  failedCount: number;
  status: 'draft' | 'running' | 'completed' | 'paused';
  variants: string[];
}

export interface DeviceSession {
  connected: boolean;
  phoneNumber?: string;
  batteryLevel?: number;
  browser?: string;
  lastActive?: string;
  statusText: string;
}
