<script>
	import { module, app } from '$lib/store.svelte.js';

	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, update } = $props();
</script>

{#if app.user.access.includes('item:edit_status')}
	<Edit_Button
		onclick={() =>
			module.open(Form, {
				key: item.key,
				status: item.status,
				files: item.files,
				update
			})}
	>
		Edit Status: <span class="status {item.status}">{item.status}</span>
	</Edit_Button>
{/if}

<style>
	.status {
		font-weight: 800;
	}
	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}
</style>
