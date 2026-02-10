<script>
	import { Datetime } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Edit from './form.svelte';

	let { item, edit_mode, update } = $props();
</script>

{#if app.user.access.includes('item:edit_date') && edit_mode}
	<Edit_Button
		onclick={() =>
			module.open(Edit, {
				key: item.key,
				date_created: item.date_created,
				update
			})}
	>
		Edit Date
	</Edit_Button>
	<div class="date">
		<Datetime datetime={item.date_created} />
	</div>
{/if}

<style>
	.date {
		font-size: 0.8rem;
	}
</style>
