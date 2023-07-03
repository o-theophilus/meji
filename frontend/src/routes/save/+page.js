import { get } from 'svelte/store';
// import { page } from '$app/stores';
// import { state, page_name } from "$lib/page_state.js"
import { token } from "$lib/cookie.js"
// import { browser } from '$app/environment';

export const load = async ({ fetch, url }) => {
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/save`)
	
	// let _page_name = "shop"
	// page_name.set(_page_name)
	// state.subscribe((value) => {
	// 	if (value[_page_name].search) {
	// 		backend.searchParams.set('search', value[_page_name].search);
	// 	}
	// 	if (value[_page_name].category) {
	// 		backend.searchParams.set('category', value[_page_name].category);
	// 	}
	// 	if (value[_page_name].status) {
	// 		backend.searchParams.set('status', value[_page_name].status);
	// 	}
	// 	if (value[_page_name].page_no) {
	// 		backend.searchParams.set('page_no', value[_page_name].page_no);
	// 	}
	// 	if (value[_page_name].order) {
	// 		backend.searchParams.set('order', value[_page_name].order);
	// 	}
	// }); 

	// // if (browser){
	// // 	page.subscribe((value) => {
	// // 		console.log("here");
	// // 		if(value.url){
	// // 			value.url.search = backend.search
	// // 			window.history.pushState(history.state, '', value.url.href);
	// // 		}
	// // 	}); 
	// // }

	// // if (url.searchParams.has('page_no')) {
	// // 	backend.searchParams.set('page_no', url.searchParams.get('page_no'));
	// // }
	// // if (url.searchParams.has('fk1') && url.searchParams.has('fv1')) {
	// // 	backend.searchParams.set('fk1', url.searchParams.get('fk1'));
	// // 	backend.searchParams.set('fv1', url.searchParams.get('fv1'));
	// // }
	
	
	// // console.log(backend.search);
	// // console.log(_page);

	

	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: get(token)
		}
	});

	resp = await resp.json();
	if (resp.status == 200) {
		return resp
    }
}
