<script>
	export let log;

	let url = '';
	if (log.entity.type == 'order') {
		url = `/orders`;
	} else if (log.entity.type == 'voucher') {
		url = `/admin/vouchers`;
	}
</script>

<section>
	{log.date} 
	<span class="status" class:error={log.status == 400}>
		{log.status}
	</span>
	<br />
	<!-- <a href="/{log.user.key}"> -->
	<a href="/profile">
		{log.user.name}
	</a>:
	{log.action}
	<a href="{url}/{log.entity.key}" data-sveltekit-preload-data="tap" >
		{#if log.entity.name}
			{log.entity.name}
		{:else}
			{log.entity.key}
		{/if}
	</a>

	{#if log.misc}
		{#each Object.entries(log.misc) as [key, value]}
			<br />
			{key}: {value}
		{/each}
	{/if}
</section>

<style>
	section {
		padding: var(--sp0) 0;
	}
	section:not(:last-child) {
		border-bottom: 2px solid var(--ac4);
	}

	.status {
		background-color: var(--cl5);
		color: var(--ac5_);
	}
	.error {
		background-color: var(--cl4);
	}
</style>
