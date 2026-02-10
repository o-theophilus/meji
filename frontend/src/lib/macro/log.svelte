<script>
	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	let { action = null, entity_key = null, entity_type = null, status = 200, misc = {} } = $props();

	onMount(() => {
		if (entity_type == 'page') {
			action = page.url.pathname;
			entity_key = `${page.url.pathname}${page.url.search}`;
		}

		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ action, entity_key, entity_type, status, misc })
		});
	});
</script>
