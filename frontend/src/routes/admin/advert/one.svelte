<script>
	import { Tag } from '$lib/button';

	let { ads, spaces, sizes } = $props();
</script>

<a href="/{ads.slug}">
	<div class="name">
		{ads.name}
	</div>

	<div class="one">
		photos
		<div class="row">
			{#each sizes as x}
				<Tag
					--tag-font-size="0.7rem"
					--tag-background-color={Object.keys(ads.photo).includes(x) ? 'green' : ''}
					--tag-color={Object.keys(ads.photo).includes(x) ? 'hsl(0, 0%, 95%)' : ''}
				>
					{x}
				</Tag>
			{/each}
		</div>
	</div>

	<div class="one">
		sizes
		<div class="row">
			{#each spaces as x}
				<Tag
					--tag-font-size="0.7rem"
					--tag-background-color={ads.space.includes(x) ? 'green' : ''}
					--tag-color={ads.space.includes(x) ? 'hsl(0, 0%, 95%)' : ''}
				>
					{x}
				</Tag>
			{/each}
		</div>
	</div>
</a>

<style>
	a {
		display: block;

		margin: 8px 0;
		padding: 16px;
		border-radius: 8px;

		background-color: var(--bg3);
		text-decoration: none;
		color: var(--ft2);
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}
	}

	.name {
		font-size: 0.8rem;
		font-weight: 800;
		color: var(--ft1);
	}

	.one {
		margin-top: 8px;
		font-size: 0.8rem;
	}

	.row {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
	}
</style>
