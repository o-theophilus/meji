<script>
	import { page } from '$app/stores';
	export let items;
</script>

<b>Item{items.length > 1 ? 's' : ''}:</b>
{#each items as x}
	<br />
	<br />
	<img
		src="{x.photo}/40"
		alt={x.name}
		style="
		width:40px; 
height: 40px; 
object-fit: cover;
margin-right:10px;
border-radius: 8px;
"
	/>
	<div
		style="
		display:inline-block;
		"
	>
		<a
			style="
text-decoration: none;
color: #1d9bf0;
font-weight: 700;
"
			href="{$page.url.origin}/{x.slug}"
			target="_blank"
		>
			{x.name}
		</a>
		<br />
		{#each Object.entries(x.variation) as [key, value], i}
			{#if i != 0},{/if}
			{key}:

			{@const v = value.split(':')}
			{#if v[0]}
				{v[0]}
			{/if}

			{#if v[1]}
				<div
					style="
		display:inline-block;
		width:16px; 
		height: 16px; 
		border:2px solid gray;
		border-radius:50%;
		background-color:{v[1]}
		"
				/>
			{/if}
		{/each}

		{#if x.quantity > 1}
			, quantity: x{x.quantity}
		{/if}
	</div>
{/each}
