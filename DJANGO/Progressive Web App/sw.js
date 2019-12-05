var cacheName = 'kvups-v01';

//the css files ind js files are cached to load in offline mode
var urlsToCacheKeys = [
	'/',
	'/static/css/ie.css',
	'/static/css/style.css',

	'/static/js/jquery.min.js',
	'/static/js/jquery.bxslider.min.js',
	'/static/js/script.js',
];

self.addEventListener('install', event =>{
	console.log(cacheName + ' installing....');
	self.skipWaiting();

	event.waitUntil(
		caches.open(cacheName).then(function(cache){
			console.log('Opened Cache');
			cache.addAll(urlsToCacheKeys.map(function(urlsToCacheKeys){
				return new Request(urlsToCacheKeys, {mode: 'no-cors'});
			})).then(function(){
				console.log('All resources have been fetched and cached.');
			});
		})
	);
});

self.addEventListener('active', function(event){
	var cacheWhitelist = ['kvups-v01',];

	event.waitUntil(
		caches.keys().then(function(cacheNames){
			return Promise.all(
				cacheNames.map(function(cacheName){
					if(cacheWhitelist.indexOf(cacheName) === -1){
						return caches.delete(cacheName);
					}
				})
			);
		})
	);
});

self.addEventListener('fetch', (event) =>{
	event.respondWith(async function(){
		const cache = await caches.open(cacheName);
		const cachedResponse = await cache.match(event.request);
		const networkResponsePromise = fetch(event.request);

		event.waitUntil(async function(){
			const networkResponse = await networkResponsePromise;
			await cache.put(event.response, networkResponse.clone());
		}());

		return cachedResponse || networkResponsePromise;
	}());
});

self.addEventListener('beforeinstallprompt', (e) => {

	e.preventDefault();
	deferredPrompt = e;
	addBtn.style.display = 'block';

	addBtn.addEventListener('click', (e) => {
		addBtn.style.display = 'none';
		deferredPrompt.prompt();

		deferredPrompt.userChoice.then((choiceResult) => {
			if (choiceResult.outcome === 'accepted') {
				console.log('User accepted the A2HS prompt');
			}
			else{
				console.log('User dismissed the A2HS prompt');	
			}
			deferredPrompt = null;
		});
	});
});