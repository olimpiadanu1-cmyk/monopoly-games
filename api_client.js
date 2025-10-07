// API клиент для работы с сервером Monopoly Game
class MonopolyAPI {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.cache = new Map(); // Кеш для данных
        this.cacheTimeout = 5000; // 5 секунд кеш
    }

    // Проверка статуса сервера
    async checkStatus() {
        try {
            const response = await fetch(`${this.baseURL}/status`);
            const result = await response.json();
            return result.success;
        } catch (error) {
            console.warn('Сервер недоступен:', error.message);
            return false;
        }
    }

    // Загрузить данные определенного типа
    async loadData(dataType) {
        try {
            // Проверяем кеш
            const cacheKey = dataType;
            const cached = this.cache.get(cacheKey);
            if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
                console.log(`📦 ${dataType} загружены из кеша`);
                return cached.data;
            }

            const response = await fetch(`${this.baseURL}/data/${dataType}`);
            const result = await response.json();
            
            if (result.success) {
                // Сохраняем в кеш
                this.cache.set(cacheKey, {
                    data: result.data,
                    timestamp: Date.now()
                });
                
                console.log(`✅ ${dataType} загружены с сервера`);
                return result.data;
            } else {
                console.error(`❌ Ошибка загрузки ${dataType}:`, result.error);
                return null;
            }
        } catch (error) {
            console.error(`❌ Ошибка загрузки ${dataType}:`, error.message);
            return null;
        }
    }

    // Сохранить данные определенного типа
    async saveData(dataType, data) {
        try {
            const response = await fetch(`${this.baseURL}/data/${dataType}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Обновляем кеш
                this.cache.set(dataType, {
                    data: data,
                    timestamp: Date.now()
                });
                
                console.log(`✅ ${dataType} сохранены на сервере`);
                return true;
            } else {
                console.error(`❌ Ошибка сохранения ${dataType}:`, result.error);
                return false;
            }
        } catch (error) {
            console.error(`❌ Ошибка сохранения ${dataType}:`, error.message);
            return false;
        }
    }

    // Загрузить все данные сразу
    async loadAllData() {
        try {
            const response = await fetch(`${this.baseURL}/all-data`);
            const result = await response.json();
            
            if (result.success) {
                // Обновляем весь кеш
                for (const [dataType, data] of Object.entries(result.data)) {
                    this.cache.set(dataType, {
                        data: data,
                        timestamp: Date.now()
                    });
                }
                
                console.log('✅ Все данные загружены с сервера');
                return result.data;
            } else {
                console.error('❌ Ошибка загрузки всех данных:', result.error);
                return null;
            }
        } catch (error) {
            console.error('❌ Ошибка загрузки всех данных:', error.message);
            return null;
        }
    }

    // Очистить кеш
    clearCache() {
        this.cache.clear();
        console.log('🗑️ Кеш очищен');
    }

    // Получить данные из кеша
    getCachedData(dataType) {
        const cached = this.cache.get(dataType);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }
}

// Создаем глобальный экземпляр API
window.monopolyAPI = new MonopolyAPI();

