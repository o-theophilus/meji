<script>
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
</script>

{#if app.user.access.includes('item:edit_name') && edit_mode}
	<Edit_Button
		onclick={() =>
			module.open(Form, {
				key: item.key,
				name: item.name,
				update
			})}
	>
		Edit Name
	</Edit_Button>
{/if}
<div class="page_title">
	{item.name}
</div>
