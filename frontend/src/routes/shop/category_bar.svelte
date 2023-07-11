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
	export let categories = [];
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<Button
			name="all"
			class="tag"
			active={!$state.shop.category}
			on:click={() => {
				$state.shop.category = '';
				// pagination.init();
				submit();
			}}
		/>
		{#each categories as category}
			<Button
				name={category.name}
				class="tag"
				active={$state.shop.category == category.name}
				on:click={() => {
					$state.shop.category = category.name;
					// pagination.init();
					submit();
				}}
			/>
		{/each}
	</div>
{/if}

<style>
	.block {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;

		margin-top: var(--sp2);
	}
</style>
