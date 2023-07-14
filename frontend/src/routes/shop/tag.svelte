<script>
	import { createEventDispatcher } from 'svelte';
	import { user, module } from '$lib/store.js';
	import { state, page_name } from '$lib/page_state.js';

	import Button from '$lib/button.svelte';
	import Add from './_add.svelte';

	let emit = createEventDispatcher();

	const submit = (status) => {
		$state[$page_name][query] = status;
		emit('ok');
	};
	export let tags = [];
</script>

<!-- {#if $user && $user.roles.includes('admin')} -->
	<div class="block">
		<Button
			name="all"
			class="tag"
			active={!$state.shop.tag}
			on:click={() => {
				$state.shop.tag = '';
				// pagination.init();
				submit();
			}}
		/>
		{#each tags as tag}
			<Button
				name={tag.name}
				class="tag"
				active={$state.shop.tag == tag.name}
				on:click={() => {
					$state.shop.tag = tag.name;
					// pagination.init();
					submit();
				}}
			/>
		{/each}
	</div>
<!-- {/if} -->

<style>
	.block {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;

		margin-top: var(--sp2);
	}
</style>
