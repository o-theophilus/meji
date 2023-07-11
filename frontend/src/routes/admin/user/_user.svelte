<script>
	import { goto } from '$app/navigation';
	import { user } from '$lib/store.js';

	export let user;
</script>

<section
	on:click={() => {
		goto(`/admin/user/${user.key}`);
	}}
>
	<img src={user.photo ? user.photo : '/image/user.png'} alt={user.name} />

	<div class="details">
		{user.name}
		<br />
		{user.email}
	</div>
</section>

<style>
	section {
		border: 2px solid var(--ac5);
		display: flex;

		border-radius: var(--brad1);
		overflow: hidden;

		cursor: pointer;
	}

	section:hover {
		border-color: var(--cl1);
	}

	img {
		--size: 80px;
		width: var(--size);
		height: var(--size);
		object-fit: cover;
	}
	.details {
		padding: var(--sp2);
	}
</style>
