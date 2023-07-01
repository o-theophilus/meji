<script>
	import { module } from '$lib/store.js';
	import Button from '$lib/comp/button.svelte';

	export let in_module;
	export let user;
</script>

<Button
	class="tiny"
	icon="edit"
	icon_size="12"
	on:click={() => {
		$module = {
			module: in_module,
			data: {
				user
			}
		};
	}}
/>
