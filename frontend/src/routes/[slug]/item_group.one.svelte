<script>
	import { app } from '$lib/store.svelte.js';
	import {  Avatar } from '$lib/macro';

	let { item, refresh } = $props();

	const prerender = (x) => {
		app.item = x;
	};
</script>

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
							class="name"
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
		

<style>


	.item {
		display: flex;
		gap: 16px;
		flex: 0 0 calc((100% - var(--gap)) / 2);
		scroll-snap-align: start;

		@media screen and (min-width: 600px) {
			& {
				flex: 0 0 calc((100% - var(--gap) * 2) / 3);
			}
		}

		& .name {
			text-decoration: none;
			color: var(--ft1);
			/* font-weight: 700; */
			font-size: 0.8rem;
			/* line-height: 100%; */

			transition: color 0.2s ease-in-out;

			&:hover {
				color: var(--cl1);
			}
		}
	}
</style>
