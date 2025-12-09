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

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import CustomAlert, { AlertType, AlertButton } from '../component/CustomAlert';
import i18n from '../i18n';

interface AlertConfig {
  type?: AlertType;
  title?: string;
  message?: string;
  buttons?: AlertButton[];
  showAnimation?: boolean;
  customAnimation?: any;
}

interface AlertContextType {
  showAlert: (config: AlertConfig) => void;
  hideAlert: () => void;
}

const AlertContext = createContext<AlertContextType | undefined>(undefined);

export const AlertProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [alertConfig, setAlertConfig] = useState<AlertConfig & { visible: boolean }>({
    visible: false,
    type: 'info',
    title: '',
    message: '',
    buttons: [],
    showAnimation: true,
  });

  const showAlert = useCallback((config: AlertConfig) => {
    setAlertConfig({
      ...config,
      visible: true,
      buttons: config.buttons || [{ text: i18n.t('common.ok'), style: 'default' }],
    });
  }, []);

  const hideAlert = useCallback(() => {
    setAlertConfig((prev) => ({ ...prev, visible: false }));
  }, []);

  return (
    <AlertContext.Provider value={{ showAlert, hideAlert }}>
      {children}
      <CustomAlert
        visible={alertConfig.visible}
        type={alertConfig.type}
        title={alertConfig.title}
        message={alertConfig.message}
        buttons={alertConfig.buttons}
        onDismiss={hideAlert}
        showAnimation={alertConfig.showAnimation}
        customAnimation={alertConfig.customAnimation}
      />
    </AlertContext.Provider>
  );
};

export const useAlert = () => {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error('useAlert must be used within an AlertProvider');
  }
  return context;
};

// Alert Service - Singleton để sử dụng như Alert.alert
class AlertServiceClass {
  private showAlertCallback?: (config: AlertConfig) => void;

  setShowAlert(callback: (config: AlertConfig) => void) {
    this.showAlertCallback = callback;
  }

  // Giống Alert.alert(title, message, buttons)
  alert(
    title: string,
    message?: string,
    buttons?: AlertButton[],
    type: AlertType = 'info'
  ) {
    if (this.showAlertCallback) {
      this.showAlertCallback({
        type,
        title,
        message,
        buttons: buttons || [{ text: i18n.t('common.ok'), style: 'default' }],
      });
    }
  }

  // Shortcuts
  success(title: string, message?: string, buttons?: AlertButton[]) {
    this.alert(title, message, buttons, 'success');
  }

  error(title: string, message?: string, buttons?: AlertButton[]) {
    this.alert(title, message, buttons, 'error');
  }

  warning(title: string, message?: string, buttons?: AlertButton[]) {
    this.alert(title, message, buttons, 'warning');
  }

  info(title: string, message?: string, buttons?: AlertButton[]) {
    this.alert(title, message, buttons, 'info');
  }

  confirm(
    title: string,
    message?: string,
    onConfirm?: () => void,
    onCancel?: () => void
  ) {
    this.alert(
      title,
      message,
      [
        {
          text: i18n.t('common.cancel'),
          style: 'cancel',
          onPress: onCancel,
        },
        {
          text: i18n.t('common.confirm'),
          style: 'default',
          onPress: onConfirm,
        },
      ],
      'confirm'
    );
  }
}

export const AlertService = new AlertServiceClass();

// HOC để inject AlertService vào AlertProvider
export const withAlertService = (Component: React.FC<any>) => {
  return (props: any) => {
    const { showAlert } = useAlert();
    
    React.useEffect(() => {
      AlertService.setShowAlert(showAlert);
    }, [showAlert]);

    return <Component {...props} />;
  };
};

