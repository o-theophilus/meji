<script>
	import { state } from '$lib/store.js';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		if ($state[$page.data.page_name]) {
			for (const x of new URLSearchParams($state[$page.data.page_name])) {
				$page.url.searchParams.set(x[0], x[1]);
			}
			window.history.replaceState(history.state, '', $page.url.href);
		}
	});
</script>
