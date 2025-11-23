import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile, updateProfile } from '../../api/profile';
import { getToken, removeToken } from '../../utils/auth';
import './style.css';

const Profile = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const token = getToken();
    if (!token) {
      navigate('/login');
      return;
    }

    loadProfile();
  }, [navigate]);

  const loadProfile = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getProfile();
      setProfile(data);
      setFullName(data.full_name || '');
    } catch (err) {
      setError('Ошибка загрузки профиля');
      if (err.response?.status === 401) {
        removeToken();
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!fullName.trim()) {
      setError('Полное имя не может быть пустым');
      return;
    }

    try {
      setSaving(true);
      setError('');
      setSuccessMessage('');
      const data = await updateProfile(fullName);
      setProfile(data);
      setSuccessMessage('Профиль успешно обновлен');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError('Ошибка сохранения профиля');
      if (err.response?.status === 401) {
        removeToken();
        navigate('/login');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const handleToChat = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="profile-card">
          <p>Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
      <div className="profile-card">
        <h1 className="profile-title">Профиль</h1>

        {error && <div className="profile-error">{error}</div>}
        {successMessage && <div className="profile-success">{successMessage}</div>}

        <div className="profile-form">
          <div className="profile-field">
            <label className="profile-label">Имя пользователя</label>
            <input
              type="text"
              className="profile-input"
              value={profile?.username || ''}
              disabled
            />
          </div>

          <div className="profile-field">
            <label className="profile-label">Полное имя</label>
            <input
              type="text"
              className="profile-input"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Введите полное имя"
            />
          </div>

          <div className="profile-buttons">
            <button
              className="profile-button profile-button-save"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Сохранение...' : 'Сохранить'}
            </button>

            <button
              className="profile-button profile-button-chat"
              onClick={handleToChat}
            >
              К чату
            </button>

            <button
              className="profile-button profile-button-logout"
              onClick={handleLogout}
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;