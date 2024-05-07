<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { goto } from '$app/navigation';
	import { user, module, loading, portal, state } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './tag_form.svelte';
	import Tag from '$lib/button/tag.svelte';
	import { onMount } from 'svelte';

	export let item = {};
	export let edit_mode = false;
	export let open = true;

	onMount(() => {
		$portal = {
			type: 'tag',
			data: {
				loaded: false,
				data: []
			}
		};
	});
</script>

{#if open}
	<div
		class="row space v_margin"
		transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
	>
		<div class="row tags">
			{#each item.tags as tag}
				<Tag
					no_grow
					on:click={() => {
						let pn = 'shop';
						let i = $state.findIndex((x) => x.name == pn);
						if (i != -1) {
							$state.splice(i, 1);
						}

						$state.push({
							name: pn,
							search: `?${new URLSearchParams({ tag }).toString()}`,
							data: [],
							loaded: false
						});

						$loading = 'loading . . .';
						goto('/shop');
					}}
				>
					{tag}
				</Tag>
			{:else}
				{#if edit_mode && $user.permissions.includes('item:edit_tag')}
					No Tag
				{/if}
			{/each}
		</div>

		{#if edit_mode && $user.permissions.includes('item:edit_tag')}
			<BRound
				icon="edit"
				icon_size="10"
				tooltip="Edit tag"
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
			/>
		{/if}
	</div>
{/if}

<style>
	.row {
		display: flex;
		gap: var(--sp1);
	}

	.space {
		align-items: center;
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}

	.tags {
		flex-wrap: wrap;
	}
</style>
