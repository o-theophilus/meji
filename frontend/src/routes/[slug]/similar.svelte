<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { app } from '$lib/store.svelte.js';
	import { FoldButton, Link } from '$lib/button';
	import { Spinner, Avatar } from '$lib/macro';

	let { group, refresh, loading } = $props();
	let open = $derived(group.open);

	const prerender = (x) => {
		app.item = x;
	};
</script>

{#if loading || group.items.length > 0}
	<div class="title line">
		<div class="line">
			{group.name}
			<Spinner active={loading} size="20" />
		</div>

		{#if !loading}
			<FoldButton
				{open}
				onclick={() => {
					open = !open;
				}}
			/>
		{/if}
	</div>

	{#if open && !loading}
		<div class="area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each group.items as item}
				<div class="item">
					<a
						href="/{item.slug}"
						onclick={() => {
							prerender(item);
							refresh(item);
						}}
						onmouseenter={() => prerender(item)}
					>
						<Avatar size="58" photo={item.photo} no_photo="/no_photo.png" name={item.name}></Avatar>
					</a>
					<div class="details">
						<a
							class="link"
							href="/{item.slug}"
							onclick={() => {
								prerender(item);
								refresh(item);
							}}
							onmouseenter={() => prerender(item)}
						>
							{item.name}
						</a>

						<div class="price">
							{#if Number(item.price)}
								₦{Number(item.price).toLocaleString()}
							{/if}
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
{/if}

<style>
	.title {
		justify-content: space-between;
		margin: 48px 0;
	}

	.area {
		display: flex;
		gap: 24px;
		/* margin: 48px 0; */
		overflow-x: auto;

		@media screen and (min-width: 600px) {
			& {
				grid-template-columns: 1fr 1fr;
			}
		}
	}

	.item {
		display: flex;
		gap: 16px;
		flex: 0 0 200px;

		& .link {
			text-decoration: none;
			color: var(--ft1);
			font-weight: 700;

			transition: color 0.2s ease-in-out;

			&:hover {
				color: var(--cl1);
			}
		}
	}
</style>
