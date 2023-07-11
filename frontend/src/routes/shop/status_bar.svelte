<script>
	import { createEventDispatcher } from 'svelte';
	import { user, module } from '$lib/store.js';
	import { state, page_name } from '$lib/page_state.js';

	import Button from '$lib/button.svelte';
	import Add from './add.svelte';

	let emit = createEventDispatcher();

	const submit = (status) => {
		$state[$page_name][query] = status;
		emit('ok');
	};
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<div class="left">
			<Button
				name={'live'}
				class="tiny"
				active={$state[$page_name]['status'] == 'live'}
				on:click={() => {
					submit('live');
				}}
			/>
			<Button
				name={'draft'}
				class="tiny"
				active={$state[$page_name]['status'] == 'draft'}
				on:click={() => {
					submit('draft');
				}}
			/>
			<Button
				name={'delete'}
				class="tiny"
				active={$state[$page_name]['status'] == 'delete'}
				on:click={() => {
					submit('delete');
				}}
			/>
		</div>
		<Button
			icon="add"
			icon_size="12"
			name="Add"
			class="tiny primary"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		/>
	</div>
{/if}

<style>
	.block,
	.left {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
	.block {
		justify-content: space-between;
		margin-top: var(--sp2);
	}
</style>
