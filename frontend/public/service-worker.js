const CACHE_NAME = 'my-solid-app-cache-v1';
const urlsToCache = [
  '/', // 缓存主页
  '/index.html', // 缓存HTML文件
  '/src/index.jsx', // 缓存 SolidJS 入口文件
  // ... 其他你希望离线可用的静态资源 (CSS, JS, 图片等)
];

// 安装阶段：缓存文件
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 激活阶段：清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  // 立即控制所有客户端，确保激活后立即生效
  event.waitUntil(self.clients.claim());
});

// 抓取阶段：拦截网络请求并提供缓存优先策略
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // 如果缓存中有，则返回缓存的资源
        if (response) {
          return response;
        }
        // 否则，从网络获取
        return fetch(event.request)
          .then((response) => {
            // 检查响应是否有效
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            // 克隆响应，因为响应流只能被消费一次
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache); // 缓存新的网络请求
              });
            return response;
          });
      })
  );
});