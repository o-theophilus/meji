<script>
	export let title;
	export let color = false;
</script>

<div class="divider" />

<section>
	<div class="title" class:color>{title}</div>
	<div class="right"><slot /></div>
</section>

<style>
	.divider:not(:first-child) {
		height: 2px;
		background-color: var(--ac5);
		margin: 0 var(--sp2);
	}

	section {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp2);

		padding: var(--sp2);
	}
	.title {
		font-weight: bold;
		color: var(--ac1);
	}
	.color {
		color: var(--cl1);
	}
	.right {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		flex-shrink: 0;
	}
</style>
